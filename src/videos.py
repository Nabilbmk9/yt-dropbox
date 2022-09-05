import os
import random
import moviepy.editor as me
from pathlib import Path
import time
import progressbar
from dotenv import load_dotenv

from dropbox_functions import _dropbox_download_file, _dropbox_list_files

load_dotenv(".env")
BASE_DIR = Path().cwd()








################################################
# UPDATED FUNCTIONS

def mixed_videos_list(dropbox_videos_path):
    stock_videos = _dropbox_list_files(dropbox_videos_path)['name']
    random.shuffle(stock_videos)
    return stock_videos


def find_keywords_in(podcast_title):
    words_in_title = podcast_title.split()
    keyword_folders = {}
    for word in words_in_title:
        if keyword_folders.get(word) is not None:
            return keyword_folders.get(word)
    return("Autre")


def dl_enough_videos_for(audio_path, dropbox_videos_path):
    audio_duration = me.AudioFileClip(audio_path).duration
    videos_list = mixed_videos_list(dropbox_videos_path)
    video_duration = 0
    print("Téléchargement des vidéos...")
    with progressbar.ProgressBar(max_value=audio_duration+100) as bar:
        for prefix, video in enumerate(videos_list, start=1):
            video_path = f"tmp/Videos/{prefix}-{video}"
            dropbox_path= f"{dropbox_videos_path}/{video}"
            _dropbox_download_file(dropbox_path, video_path)
            video_duration += me.VideoFileClip(video_path).duration
            bar.update(video_duration)
            if video_duration >= audio_duration:
                return


def video_editing(video_folder_path, video_title):
    clip = []
    for video_file in Path(video_folder_path).iterdir():
        clip.append(me.VideoFileClip(f"{video_file.parent}/{video_file.name}", audio=False, target_resolution=(720, 1280)).crossfadein(1))

    final_clip = me.concatenate(clip, padding=-1, method="compose")
    final_clip.write_videofile(f"tmp/Output/{video_title}.mp4")
    return f"tmp/Output/{video_title}.mp4"


def add_audio_on_video(path_videoclip, path_audioclip):
    podcast_name = Path(path_audioclip).stem

    videoclip = me.VideoFileClip(path_videoclip).without_audio()
    audioclip = me.AudioFileClip(path_audioclip)

    new_audioclip = me.CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip
    videoclip = videoclip.set_duration(audioclip.duration)
    videoclip.write_videofile(f"tmp/Output/{podcast_name}.mp4")
    audioclip.close()
    return f"tmp/Output/{podcast_name}.mp4"


def create_video(podcast):
    #Download the podcast
    os.makedirs("tmp/Podcast", exist_ok=True)
    local_podcast_path = "tmp/Podcast/" + podcast['title'] + ".mp3"
    _dropbox_download_file(podcast['path'], local_podcast_path)

    #Download the videos
    os.makedirs("tmp/Videos", exist_ok=True)
    dropbox_videos_path = os.getenv("DROPBOX_VIDEO_PATH") + "/" + find_keywords_in(podcast['title'])
    dl_enough_videos_for(local_podcast_path, dropbox_videos_path)

    #Video montage
    os.makedirs("tmp/Output", exist_ok=True)
    final_video_path = video_editing("tmp/Videos", podcast['title'])

    #Add audio in the video
    final_video_path = add_audio_on_video(final_video_path, local_podcast_path)

    return final_video_path


if __name__ == '__main__':
    podcast = {"title": "Test", "path": "/Podcasts/2020-10-01 - Test.mp3"}
    dropbox_videos_path = os.getenv("DROPBOX_VIDEO_PATH") + "/" + find_keywords_in(podcast['title'])
    print(dropbox_videos_path)
