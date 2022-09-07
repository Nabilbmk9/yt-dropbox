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
    return("default")


def dl_enough_videos_for(audio_path, dropbox_videos_path):
    # Return if enough videos are already downloaded in local folder
    downloaded_videos = os.listdir("tmp/Videos")
    downloaded_videos = [video for video in downloaded_videos if video.endswith(".mp4")]
    videos_duration = 0
    audio_duration = me.AudioFileClip(audio_path).duration 
    for video in downloaded_videos:
        videos_duration += me.VideoFileClip(f"tmp/Videos/{video}").duration
        if videos_duration >= audio_duration:
            print("Enough videos already downloaded")
            return
    
    audio_duration = me.AudioFileClip(audio_path).duration
    videos_list = _dropbox_list_files(dropbox_videos_path)['name']
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


def edit_final_video(video_folder_path, video_title):
    clips = []
    for video_file in Path(video_folder_path).iterdir():
        clips.append(me.VideoFileClip(f"{video_file.parent}/{video_file.name}", audio=False, target_resolution=(720, 1280)).crossfadein(1))

    final_clip = me.concatenate_videoclips(clips, padding=-1, method="compose")
    final_clip.write_videofile(f"tmp/Output/_{video_title}.mp4")
    return f"tmp/Output/_{video_title}.mp4"

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
    dropbox_videos_path = os.getenv("STOCK_VIDEOS_PATH") + find_keywords_in(podcast['title'])
    dl_enough_videos_for(local_podcast_path, dropbox_videos_path)

    #Video montage
    if not os.path.exists(f"tmp/Output/_{podcast['title']}.mp4"):
        os.makedirs("tmp/Output", exist_ok=True)
        final_video_path = edit_final_video("tmp/Videos", podcast['title'])
    else:
        final_video_path = f"tmp/Output/_{podcast['title']}.mp4"
        print("Video without audio already exists")

    #Add audio in the video
    if not os.path.exists(f"tmp/Output/{podcast['title']}.mp4"):
        final_video_path = add_audio_on_video(final_video_path, local_podcast_path)
    else:
        final_video_path = f"tmp/Output/{podcast['title']}.mp4"
        print("Video with audio already exists")

    return final_video_path


if __name__ == '__main__':
    podcast = {"title": "Test", "path": "/Podcasts/2020-10-01 - Test.mp3"}
    dropbox_videos_path = os.getenv("STOCK_VIDEOS_PATH") + find_keywords_in(podcast['title'])
    print(dropbox_videos_path)
