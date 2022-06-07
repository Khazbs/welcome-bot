from itertools import count
from operator import itemgetter
from PIL import Image, ImageDraw, ImageFont
import io
import json
import random

TEMPLATES_DIR = 'src/templates/'
FONT_PATH = TEMPLATES_DIR + 'nunito600.ttf'


def get_random_template():
	templates = json.load(open(TEMPLATES_DIR + 'templates.json', 'r'))
	return random.choice(templates)


def emboss_username(image, textbox, username):
	draw = ImageDraw.Draw(image)
	x, y, w, h = itemgetter('x', 'y', 'w', 'h')(textbox)
	# draw.rectangle((x, y, x + w, y + h), outline='red', width=10)
	old_font = ImageFont.truetype(FONT_PATH, 1)
	for i in count(2):
		font = ImageFont.truetype(FONT_PATH, i)
		tw, th = draw.textsize(username, font)
		if (tw > w or th > h):
			x_center, y_bottom = x + (w - tw) // 2, y + (h - th)
			draw.text((x_center, y_bottom), username, 'white', old_font)
			break
		old_font = font


async def open_image(path):
	return Image.open(path)


async def save_image(image, fp, format):
	return image.save(fp, format)


async def finalize_image(image):
	bio = io.BytesIO()
	await save_image(image, bio, 'png')
	bio.seek(0)
	return bio


async def make(username):
	template = get_random_template()
	image = await open_image(TEMPLATES_DIR + template['image'])
	emboss_username(image, template['textbox'], '@' + username)
	return await finalize_image(image)
