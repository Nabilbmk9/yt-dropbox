import time, random, os
from datetime import datetime, timedelta
from pathlib import Path
import moviepy.editor as me
from dotenv import load_dotenv

from rss import *
from dropbox_functions import *
from videos import *
from youtube import *
from helpers import *

load_dotenv(".env")

latest_video = get_latest_video_on_yt(os.getenv("YT_PLAYLIST_ID")) # -> "The latest video on youtube"

podcasts_path = os.environ.get("PODCASTS_PATH") # -> "/Podcast"
new_podcasts = get_new_podcasts(podcasts_path, latest_video['title'])
# -> new_podcasts = [{title: "Title", description: "", path: "/Podcast/title.mp3", tags: ["paix", "amour"], publication_date: ""}, {}, {}]

for podcast in new_podcasts:
    tags_and_descriptions = get_tags_and_description_from_rss(podcast['title'])
    podcast['description'] = tags_and_descriptions[0]
    podcast['tags'] = tags_and_descriptions[1]

if new_podcasts == []:
    print("No new podcast")
    exit()

print(f"{len(new_podcasts)} new podcasts found...")

last_youtube_publication_date = get_last_youtube_publication_date(latest_video['id']) # -> "The last youtube publication date"

for extra_days, podcast in enumerate(new_podcasts, start=1):
    publication_date = publish_time(last_youtube_publication_date + timedelta(days=extra_days), post_time_hour=int(os.getenv("POST_TIME_HOUR")))
    podcast['publication_date'] = yt_format_date(publication_date)

for new_podcast in new_podcasts:
    print(f"Processing {new_podcast['title']}...")
    video_path = create_video(new_podcast)
    exit()
    thumbnail_path = create_thumbnail(video_path, new_podcast)
    upload_video_to_youtube(video_path, thumbnail_path, new_podcast)
    delete_video_and_thumbnail(video_path, thumbnail_path)
    print(f"{new_podcast} processed")

