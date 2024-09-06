import json
import shutil
from datetime import datetime
import discord
import tiktoken
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import openai
from creds import org, api_key
import os

model_multipliers = {
    'gpt-3.5-turbo': (0.0015 / 1000, 0.002 / 1000),
    'gpt-3.5-turbo-16k': (0.003 / 1000, 0.004 / 1000),
    'gpt-4': (0.03 / 1000, 0.06 / 1000),
    'gpt-4-32k': (0.06 / 1000, 0.12 / 1000),
    'dalle': (0, 0.02)
}


async def gpt(interaction, text, messages):

    if not has_subscription(interaction):
        await interaction.followup.send("This command is exclusive to subscribers. See https://discord.com/channels/1118288278622310433/1149856144890794106 to learn more.")
        return

    if not has_credits(str(interaction.user.id)):
        await interaction.followup.send("You have no remaining credits. See https://discord.com/channels/1118288278622310433/1149856144890794106 to learn more.")
        return

    model = set_model(text)
    organization = org
    openai.api_key = api_key
    response = openai.ChatCompletion.create(model=model, messages=messages)

    await send_message(interaction, response["choices"][0]["message"]['content'])
    update_usage(userid=interaction.user.id, itokens=response['usage']['prompt_tokens'], otokens=response['usage']['completion_tokens'], model=model)


def set_model(text):
    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
    num_tokens = len(encoding.encode(text))
    if num_tokens > 4096:
        return 'gpt-3.5-turbo-16k'
    return 'gpt-3.5-turbo'


async def init_scan(interaction, file):
    if file.filename[-4:].lower() in ['.png', '.jpg', 'jpeg']:
        return await save_and_scan_image(interaction, file)
    elif file.filename[-4:].lower() == '.pdf':
        return await save_and_scan_pdf(interaction, file)
    else:
        await interaction.followup.send("This file type is not supported. Please use an image or pdf.")
        return 'failed'


def scan(imgpath):
    text = ''
    img = Image.open(imgpath)
    new_size = tuple(2 * x for x in img.size)
    img = img.resize(size=new_size, resample=Image.LANCZOS)
    text += pytesseract.image_to_string(img)
    return text


async def save_and_scan_image(interaction, file):
    dirpath = os.path.join('/Users/misterrobot/Desktop/Programming/Rice Farmer', interaction.user.name)
    filepath = os.path.join(dirpath, 'image.png')

    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)

    os.makedirs(dirpath)

    await file.save(filepath)
    text = scan(filepath)
    shutil.rmtree(dirpath)

    return text


async def save_and_scan_pdf(interaction, file):
    pdfdirpath = os.path.join('/Users/misterrobot/Desktop/Programming/Rice Farmer', interaction.user.name + 'pdf')
    dirpath = os.path.join('/Users/misterrobot/Desktop/Programming/Rice Farmer', interaction.user.name)
    filepath = os.path.join(pdfdirpath, 'pdf.pdf')

    if os.path.exists(pdfdirpath) and os.path.isdir(pdfdirpath):
        shutil.rmtree(pdfdirpath)
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)

    os.makedirs(dirpath)
    os.makedirs(pdfdirpath)

    await file.save(filepath)
    images = convert_from_path(filepath, output_folder=dirpath)

    text = ''
    for img in os.listdir(dirpath):
        text += scan(os.path.join(dirpath, img))

    shutil.rmtree(pdfdirpath)
    shutil.rmtree(dirpath)

    return text


def update_usage(userid, itokens, otokens, model):
    uid = str(userid)
    imult, omult = model_multipliers.get(model, (0, 0))

    with open('userlog.json', 'r') as file:
        user_profiles = json.load(file)

    cost = itokens * imult + otokens * omult
    user_profiles[uid]['used'] += cost * 1000

    with open('userlog.json', 'w') as outfile:
        json.dump(user_profiles, outfile, indent=4)


async def send_message(interaction, response):
    max_length = 2000

    if len(response) > max_length:
        num_splits = len(response) // max_length

        for i in range(num_splits + 1):
            start_index = i * max_length
            end_index = (i + 1) * max_length
            await interaction.followup.send(response[start_index:end_index])
    else:
        await interaction.followup.send(response)


def has_credits(userid):
    uid = str(userid)
    with open('userlog.json', 'r') as file:
        user_profiles = json.load(file)

    used = user_profiles[uid]['used']
    available = user_profiles[uid]['available']

    return used < available


async def create_profile(interaction, userid, tier):
    uid = str(userid)
    try:
        with open('userlog.json', 'r') as file:
            user_profiles = json.load(file)
    except:
        user_profiles = {}

    if uid not in user_profiles:
        if tier == 'monkey': user_profiles[uid] = {'used': 0, 'available': 100}
        elif tier == 'basic': user_profiles[uid] = {'used': 0, 'available': 1000}
        elif tier == 'standard': user_profiles[uid] = {'used': 0, 'available': 2500}
        elif tier == 'pro': user_profiles[uid] = {'used': 0, 'available': 5000}
        else: return False

        with open('userlog.json', 'w') as outfile:
            json.dump(user_profiles, outfile, indent=4)

        await interaction.followup.send('Subscription successfully activated.')
        return True
    else:
        if tier == 'monkey': user_profiles[uid]['available'] = 100
        elif tier == 'basic': user_profiles[uid]['available'] = 1000
        elif tier == 'standard': user_profiles[uid]['available'] = 2500
        elif tier == 'pro': user_profiles[uid]['available'] = 5000
        else: return False

        with open('userlog.json', 'w') as outfile:
            json.dump(user_profiles, outfile, indent=4)

        await interaction.followup.send(f"Available credits set to {user_profiles[uid]['available']}.")
        return True


def has_subscription(interaction):
    tier_names = ['Monkey Tier', 'Basic Tier', 'Standard Tier', 'Pro Tier']

    for tier_name in tier_names:
        tier_role = discord.utils.find(lambda r: r.name == tier_name, interaction.guild.roles)
        if tier_role in interaction.user.roles: return True
    return False


def has_paid_subscription(interaction):
    tier_names = ['Basic Tier', 'Standard Tier', 'Pro Tier']
    for tier_name in tier_names:
        tier_role = discord.utils.find(lambda r: r.name == tier_name, interaction.guild.roles)
        if tier_role in interaction.user.roles: return True
    return False


def get_tier(interaction):
    tier_roles = {
        'Monkey Tier': 'monkey',
        'Basic Tier': 'basic',
        'Standard Tier': 'standard',
        'Pro Tier': 'pro'
    }

    for role_name, tier_name in tier_roles.items():
        role = discord.utils.find(lambda r: r.name == role_name, interaction.guild.roles)
        if role in interaction.user.roles: return tier_name

    return None


def backup_data():
    json_file_path = 'userlog.json'
    backup_file_path = 'backup_userlog.json'
    backup_consolelog_path = 'backup_consolelog.txt'

    with open(json_file_path, 'r') as file:
        user_profiles = json.load(file)

    try:
        with open(backup_file_path, 'r') as file:
            backup_profiles = json.load(file)
    except:
        backup_profiles = {}

    if len(user_profiles.items()) > 0:
        for uid, data in user_profiles.items():
            if uid not in backup_profiles:
                backup_profiles[uid] = {'used': data['used'], 'available': data['available']}
            else:
                backup_profiles[uid]['used'] += data['used']
                backup_profiles[uid]['available'] += data['available']

        with open(backup_file_path, 'w') as backup_file:
            json.dump(backup_profiles, backup_file, indent=4)

    with open(json_file_path, 'w') as file:
        json.dump({}, file, indent=4)

    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(backup_consolelog_path, 'a') as backup_consolelog:
        backup_consolelog.write(f"{current_date} - Data appended to '{backup_file_path}'." + '\n')
        backup_consolelog.write('Data transferred: ' + str(user_profiles) + '\n\n')
