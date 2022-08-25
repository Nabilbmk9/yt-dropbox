import time, random, os
from datetime import datetime, timedelta
from pathlib import Path
from dropbox_code import dropbox_list_files, dropbox_download_file
from video_code import type_de_video_par_mot_cle, clip_transition_foudu, ajouter_audio_sur_video, \
    image_from_video, draw_multiline_in_image
import moviepy.editor as me
from youtube_code import telecharger_sur_youtube, retrieve_lastest_title_and_date_video
from autres_fonctions import publish_next_day_at_6, pending_podcasts, delete_files_in_folder


BASE_DIR = Path().cwd()
today = datetime.now().replace(microsecond=0)

run = True
while run :
    # Variable utile
    last_youtube_video_posted = retrieve_lastest_title_and_date_video()[0]
    last_video_programmed_date = retrieve_lastest_title_and_date_video()[1]
    publication_date = publish_next_day_at_6(last_video_programmed_date)

    # Récupérer la liste des podcasts sur dropbox
    liste_podcast_dropbox = dropbox_list_files("/Podcast")
    print(liste_podcast_dropbox)

    # Nombre de podcast en attente
    pending_podcast = pending_podcasts(liste_podcast_dropbox, last_youtube_video_posted)
    print(f"Il y a {pending_podcast} en attente")

    # S'il n'y a pas de nouveau podcast. Pause de 12h
    if pending_podcasts(liste_podcast_dropbox, last_youtube_video_posted) == 0:
        print("Pas de nouveau podcast. Pause de 12h")
        time.sleep(43200)

    else:
        print(f"Il y a {pending_podcast} podcast en attente")
        podcast_to_download = "".join(list(liste_podcast_dropbox.iloc[pending_podcast-1]['name']))
        titre_video_a_upload = "".join(list(liste_podcast_dropbox.iloc[pending_podcast-1]['name']))[13:-4]

        # Télécharger le podcast dans dossier nomer "Podcast"
        os.makedirs("Podcast", exist_ok=True)
        print("Téléchargement du podcast...")
        dropbox_download_file(f"/Podcast/{podcast_to_download}",
                              f"Podcast/{titre_video_a_upload}.mp3")

        # Récupérer le theme de video
        dossier_video = type_de_video_par_mot_cle(titre_video_a_upload.split(" "))
        dropbox_path_video = f"/video/{dossier_video}"

        # récupérer la liste des videos du theme du podcast
        liste_video_montage = dropbox_list_files(dropbox_path_video)['name']
        liste_video = []
        for video in liste_video_montage:
            liste_video.append(video)
        random.shuffle(liste_video)

        os.makedirs("Video", exist_ok=True)

        # Télécharger les videos pour le montage video
        podcast_a_monter = me.AudioFileClip(f"Podcast/{titre_video_a_upload}.mp3")
        print("Téléchargement des videos...")
        dropbox_download_file(f"{dropbox_path_video}/{liste_video[0]}",
                              f"Video/{liste_video.pop(0)}")
        audio_duration = podcast_a_monter.duration
        clip_duration = 0
        chiffre = 1

        while clip_duration < audio_duration:
            clip_duration = 0
            dropbox_download_file(f"{dropbox_path_video}/{liste_video[0]}",
                                  f"Video/{str(chiffre) + liste_video.pop(0)}")
            chiffre += 1
            for path in Path("Video").iterdir():

                clip = me.VideoFileClip(f"Video/{path.name}", audio=False, target_resolution=(720, 1280))
                clip_duration += clip.duration
            print(clip_duration)


        # Montage des videos
        os.makedirs("Output", exist_ok=True)
        for x in Path("Podcast").iterdir():
            path_podcast = x
            break
        output_videoclip = clip_transition_foudu("Video", titre_video_a_upload)
        ajouter_audio_sur_video(output_videoclip, f"{path_podcast.parent}/{path_podcast.name}")

        # Faire le Thumbnail
        image_thumbnail = image_from_video(output_videoclip)
        thumbnail = draw_multiline_in_image(image_thumbnail, titre_video_a_upload)

        # Upload la video sur youtube (Bonne date, flux RSS)
        telecharger_sur_youtube(publication_date, titre_video_a_upload, f"Output/{titre_video_a_upload}.mp4")

        # Vider tous les dossiers
        podcast_a_monter.close()
        clip.close()
        liste_de_dossier = ["Podcast", "Video", "Thumbnails", "Output"]
        delete_files_in_folder(liste_de_dossier)

        run = False

