import os
import moviepy.editor as me
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap

# Parameter for thumbnail
BACKGROUND_TINT_COLOR = (0, 0, 0)  # Black
TRANSPARENCY = .40  # Degree of transparency, 0-100%
TEXT_COLOR = (255, 255, 255)  # White
FONT = 'Oswald.ttf'


def image_from_video(path_videoclip):

    clip = me.VideoFileClip(path_videoclip)
    frame = clip.get_frame(5)
    os.makedirs("Thumbnail", exist_ok=True)
    new_img_filepath = "tmp/Thumbnail/thumb.jpg"
    new_img = Image.fromarray(frame)
    new_img = new_img.resize((1280, 720))
    new_img.save(new_img_filepath)
    clip.close()
    return new_img_filepath


def draw_multiline_in_image(image_path, text, size_font=100, text_color=TEXT_COLOR, text_start_height=200):
    OPACITY = int(255 * TRANSPARENCY)
    print(len(text))
    image = Image.open(image_path)
    image = image.convert("RGBA")

    # Font size according to the number of characters
    if len(text) < 40:
        size_font = 120
    elif len(text) < 50:
        size_font = 110
    elif len(text) < 60:
        size_font = 95
    else:
        size_font = 85

    font = ImageFont.truetype(FONT, size_font)
    image_width, image_height = image.size
    y_text = text_start_height

    width_text = 1
    size_width_text = 0
    while size_width_text < 1000:
        width_text += 1
        lines = textwrap.wrap(text.upper(), width=width_text)
        size_width_text = font.getsize(lines[0])[0]

    overlay = Image.new('RGBA', image.size, BACKGROUND_TINT_COLOR + (0,))
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
    image.save("result.jpg")


def create_thumbnail(video_path, text):
    pass


if __name__ == '__main__':
    pass