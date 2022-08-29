import os

import moviepy.editor as me
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
BASE_DIR = Path().cwd()

# Parameter for thumbnail
BACKGROUND_TINT_COLOR = (0, 0, 0)  # Black
TRANSPARENCY = .40  # Degree of transparency, 0-100%
TEXT_COLOR = (255, 255, 255)  # White
FONT = 'Oswald.ttf'


def ajouter_audio_sur_video(path_videoclip, path_audioclip, loop=False):
    """Prend une video et ajoute le son.
    Loop = False : La video se fige avec la derniere frame jusqu'a la fin de l'audio
    Loop = True : La video tourne en boucle jusqu'a la fin de l'audio"""

    nom_podcast = Path(path_audioclip).stem

    videoclip = me.VideoFileClip(path_videoclip).without_audio()
    audioclip = me.AudioFileClip(path_audioclip)

    if loop:
        concatenate = [videoclip, videoclip]
        while videoclip.duration < audioclip.duration:
            final = me.concatenate_videoclips(concatenate).crossfadein(1)
            clip1 = me.VideoFileClip(path_videoclip)
            concatenate.append(clip1)
            videoclip = final

    new_audioclip = me.CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip
    videoclip = videoclip.set_duration(audioclip.duration)
    videoclip.write_videofile(f"Output/{nom_podcast}.mp4")
    audioclip.close()
    return f"Output/{nom_podcast}.mp4"


def clip_transition_foudu(path_fodler, titre_video):
    clip = []
    for fichier_video in Path(path_fodler).iterdir():
        clip.append(me.VideoFileClip(f"{fichier_video.parent}/{fichier_video.name}", audio=False, target_resolution=(720, 1280)).crossfadein(1))

    clip_final = me.concatenate(clip, padding=-1, method="compose")
    clip_final.write_videofile(f"Output/-{titre_video}.mp4")
    return f"Output/-{titre_video}.mp4"


def type_de_video_par_mot_cle(liste_titre_podcast):
    dossier_mot_cle = {}

    for mot in liste_titre_podcast:
        if dossier_mot_cle.get(mot) is not None:
            return dossier_mot_cle.get(mot)
    return("Autre")


def image_from_video(path_videoclip):
    """ Télécharge l'image a 10 secondes de la video """

    clip = me.VideoFileClip(path_videoclip)
    duration = clip.duration
    max_duration = int(duration) + 1
    for i in range(max_duration):
        if i == 10:
            print(f"frame at {i} seconds")
            frame = clip.get_frame(int(i))
            os.makedirs("Thumbnails", exist_ok=True)
            new_img_filepath = "Thumbnails/thumb.jpg"
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