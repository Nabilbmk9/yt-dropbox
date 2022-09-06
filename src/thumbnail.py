import os
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


def create_thumbnail(video_path, video_title):
    screenshot = get_frame_from_video(video_path, 5)
    thumbnail = draw_text_with_shadow_on_image(screenshot, video_title)
    thumbnail.save("tmp/Thumbnail/thumbnail.jpg")
    return "tmp/Thumbnail/thumbnail.jpg"

def draw_text_with_shadow_on_image(image, text):
    image_converted = image.convert("RGBA")
    image_size = image_converted.size
    shadow_overlay = Image.new('RGBA', image_size)

    draw_text_on_image(shadow_overlay ,text, text_color=(0, 0, 0))
    blurred = shadow_overlay.filter(ImageFilter.BoxBlur(7))

    draw_text_on_image(blurred, text)

    blurred = Image.alpha_composite(image_converted, blurred)
    blurred = blurred.convert("RGB")
    blurred.save("tmp/Thumbnail/thumbnail.jpg")
    return blurred


def draw_text_on_image(image, text, font=ImageFont.truetype(FONT, 80), text_color=TEXT_COLOR, text_start_height=200):

    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height
    lines = textwrap.wrap(text, width=40)
    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(((image_width - line_width) / 2, y_text), 
                  line, font=font, fill=text_color)
        y_text += line_height


   










