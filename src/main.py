import time, random, os
from datetime import datetime, timedelta
from pathlib import Path
import moviepy.editor as me
from dotenv import load_dotenv

from rss import *
from dropbox_functions import *
from videos import *
from helpers import *
from thumbnail import *

load_dotenv(".env")
handle_arguments()

from youtube import *

latest_video = get_latest_video_on_yt(os.getenv("YT_PLAYLIST_ID"))
last_youtube_publication_date = get_last_youtube_publication_date(latest_video['id'])
print(f"Last youtube publication date: {last_youtube_publication_date}")

podcasts_path = os.environ.get("PODCASTS_PATH")
new_podcasts = get_new_podcasts(podcasts_path, latest_video['title'])

for podcast in new_podcasts:
    tags_and_descriptions = get_tags_and_description_from_rss(podcast['title'])
    podcast['description'] = tags_and_descriptions[0]
    podcast['tags'] = tags_and_descriptions[1]

if new_podcasts == []:
    print("No new podcast")
    exit()

print(f"{len(new_podcasts)} new podcasts found...")

print("In queue:")
new_podcasts.reverse()
for i, podcast in enumerate(new_podcasts, start=1):
    print(f"{i} - {podcast['title']}")

for extra_days, podcast in enumerate(new_podcasts, start=1):
    publication_date = publish_time(last_youtube_publication_date + timedelta(days=extra_days), post_time_hour=int(os.getenv("POST_TIME_HOUR")))
    podcast['publication_date'] = yt_format_date(publication_date)

for new_podcast in new_podcasts:
    print(f"Processing {new_podcast['title']}...")
    video_path = create_video(new_podcast)
    thumbnail_path = create_thumbnail(video_path, new_podcast['title'])
    upload_video_to_youtube(new_podcast, video_path, thumbnail_path)
    print(f"{new_podcast} processed")
    delete_tmp_files()