import os
import moviepy.editor as me
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
from dotenv import load_dotenv

load_dotenv(".env")

# Parameter for thumbnail
TEXT_COLOR = (255, 255, 255)  # White
FONT = 'assets/' + str(os.getenv('CHARACTERE_FONT'))

print(FONT)

def image_from_video(path_videoclip):
    clip = me.VideoFileClip(path_videoclip)
    frame = clip.get_frame(5)
    os.makedirs("tmp/Thumbnail", exist_ok=True)
    new_img_filepath = "tmp/Thumbnail/thumb.jpg"
    new_img = Image.fromarray(frame)
    new_img = new_img.resize((1280, 720))
    new_img.save(new_img_filepath)
    clip.close()
    return new_img_filepath


def draw_multiline_in_image(image_path, text, text_color=TEXT_COLOR, text_start_height=200):
    

    # Font size according to the number of characters
    if len(text) < 40:
        size_font = 120
    elif len(text) < 50:
        size_font = 110
    elif len(text) < 60:
        size_font = 95
    else:
        size_font = 85

    image = Image.open(image_path)
    image = image.convert("RGBA")

    font = ImageFont.truetype(FONT, size_font)
    image_width, image_height = image.size
    y_text = text_start_height

    
    width_text = 1
    size_width_text = 0
    while size_width_text < 1000:
        width_text += 1
        lines = textwrap.wrap(text.upper(), width=width_text)
        size_width_text = font.getsize(lines[0])[0]

    overlay = Image.new('RGBA', image.size)
    for line in lines:
        line_width, line_height = font.getsize(line)

        # Create piece of canvas to draw text on and blur
        blurred = Image.new('RGBA', image.size)
        draw = ImageDraw.Draw(blurred)
        draw.text(((image_width - line_width) / 2, y_text),
                  line, fill='black', font=font)
        blurred = blurred.filter(ImageFilter.BoxBlur(7))

        # Paste soft text onto background
        image.paste(blurred,blurred)

        draw_rect = ImageDraw.Draw(overlay)

        draw_rect.text(((image_width - line_width) / 2, y_text),
                  line, font=font, fill=text_color)
        y_text += line_height
    image = Image.alpha_composite(image, overlay)
    image = image.convert("RGB")
    image.save(image_path)
    return image_path


def create_thumbnail(video_path, text):
    image = image_from_video(video_path)
    return draw_multiline_in_image(image, text)


######################################################################################
# The functions below are being modified

def overlay_text(image, text):
    image = Image.open(image)
    image = image.convert("RGBA")
    overlay = Image.new('RGBA', image.size)
    draw = ImageDraw.Draw(overlay)
    image_width, image_height = image.size
    y_text = 200
    lines = textwrap.wrap(text, width=40)
    font = ImageFont.truetype(FONT, 80)
    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(((image_width - line_width) / 2, y_text), 
                  line, font=font, fill=(0,0,0))
        y_text += line_height
    blurred = overlay.filter(ImageFilter.BoxBlur(7))
    blurred = Image.alpha_composite(image, blurred)
    blurred = blurred.convert("RGB")
    blurred.save("result_blurred.jpg")


def draw_multiple_line_text(image_path, text, font=ImageFont.truetype(FONT, 80), text_color=TEXT_COLOR, text_start_height=200):

    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height
    lines = textwrap.wrap(text, width=40)
    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(((image_width - line_width) / 2, y_text), 
                  line, font=font, fill=text_color)
        y_text += line_height
    image.save("result.jpg")





if __name__ == "__main__":
    path = image_from_video(r"C:\Users\boulm\Downloads\Grasssss - 66810 s(1s)s.mp4")
    draw_multiline_in_image(path, "Bonjour la famile ceci est un test pour voir si ça marche bien")
   










