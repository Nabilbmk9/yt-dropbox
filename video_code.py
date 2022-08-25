import os

import moviepy.editor as me
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap
BASE_DIR = Path().cwd()


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


def draw_multiline_in_image(image_path, text, text_color=(255, 255, 255), text_start_height=200):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('Oswald.ttf', 80)
    image_width, image_height = image.size
    y_text = text_start_height
    lines = textwrap.wrap(text.upper(), width=35)
    print(lines)
    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(((image_width - line_width) / 2, y_text),
                  line, font=font, fill=text_color, stroke_width=2, stroke_fill='black')
        y_text += line_height

    image.save(image_path)
