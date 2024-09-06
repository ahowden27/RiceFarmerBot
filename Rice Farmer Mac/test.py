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
import time


def scan(imgpath):
    text = ''
    img = Image.open(imgpath)
    new_size = tuple(2 * x for x in img.size)
    img = img.resize(size=new_size, resample=Image.LANCZOS)
    text += pytesseract.image_to_string(img)
    return text


def save_and_scan_pdf():
    pdfdirpath = os.path.join('/Users/misterrobot/Desktop/Programming/Rice Farmer', 'pxkka' + 'pdf')
    dirpath = os.path.join('/Users/misterrobot/Desktop/Programming/Rice Farmer', 'pxkka')
    filepath = os.path.join(pdfdirpath, 'pdf.pdf')

    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)

    os.makedirs(dirpath)

    images = convert_from_path(filepath, output_folder=dirpath)

    text = ''
    for img in os.listdir(dirpath):
        text += scan(os.path.join(dirpath, img))

    shutil.rmtree(dirpath)

    print('text' + text)

save_and_scan_pdf()