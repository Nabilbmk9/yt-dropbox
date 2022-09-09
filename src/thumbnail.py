import os
from turtle import width
import moviepy.editor as me
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(".env")

# Parameter for thumbnail
TEXT_COLOR = (255, 255, 255)  # White
FONT = 'assets/' + str(os.getenv('CHARACTER_FONT'))


def get_frame_from_video(path_videoclip, seconds):
    clip = me.VideoFileClip(path_videoclip)
    frame = clip.get_frame(seconds)
    os.makedirs("tmp/Thumbnail", exist_ok=True)
    new_img = Image.fromarray(frame)
    new_img = new_img.resize((1280, 720))
    clip.close()
    return new_img

def draw_text_on_image(image, text, text_color=TEXT_COLOR, text_start_height=200):
    font_size = adjust_font_size_to_size_text(text)
    font = ImageFont.truetype(FONT, font_size)
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height

    lines = set_lines(font, text)

    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(((image_width - line_width) / 2, y_text), 
                  line, font=font, fill=text_color)
        y_text += line_height


def adjust_font_size_to_size_text(text):
    font_size = (140 - len(text))
    if font_size < 70:
        font_size = 70
    elif font_size > 110:
        font_size = 110
    return font_size


def set_lines(font, text):
    width = 60
    lines = textwrap.wrap(text, width)

    while any(font.getsize(line)[0] > 1240 for line in lines):
        lines = textwrap.wrap(text, width)
        width -= 1
    return lines

def draw_text_with_shadow_on_image(image, text):
    image_converted = image.convert("RGBA")
    image_size = image_converted.size
    shadow_overlay = Image.new('RGBA', image_size)

    draw_text_on_image(shadow_overlay ,text.upper(), text_color=(0, 0, 0))
    blurred = shadow_overlay.filter(ImageFilter.BoxBlur(7))

    draw_text_on_image(blurred, text.upper())

    blurred = Image.alpha_composite(image_converted, blurred)
    blurred = blurred.convert("RGB")
    blurred.save("tmp/Thumbnail/thumbnail.jpg")
    return blurred


def create_thumbnail(video_path, video_title):
    screenshot = get_frame_from_video(video_path, 5)
    thumbnail = draw_text_with_shadow_on_image(screenshot, video_title)
    os.makedirs("tmp/Thumbnail", exist_ok=True)
    thumbnail.save("tmp/Thumbnail/thumbnail.jpg")
    return "tmp/Thumbnail/thumbnail.jpg"