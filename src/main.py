import time, random, os
from datetime import datetime, timedelta
from pathlib import Path
import moviepy.editor as me

from rss import *
from dropbox_functions import *
from videos import *
from youtube import *
from helpers import *


latest_video_title = get_latest_video_on_yt(os.getenv("YT_PLAYLIST_ID"))['title'] # -> "The latest video on youtube"

podcasts_path = os.environ.get("PODCASTS_PATH") # -> "/Podcast"
new_podcasts = get_new_podcasts(podcasts_path, latest_video_title)
# -> new_podcasts = [{title: "Title", description: "", path: "/Podcast/title.mp3", tags: ["paix", "amour"], publication_date: ""}, {}, {}]

for podcast in new_podcasts:
    podcast['description'] = get_tags_and_description_from_rss(podcast['title'])[0]
    podcast['tags'] = get_tags_and_description_from_rss(podcast['title'])[1]

if new_podcasts == []:
    print("No new podcast")
    exit()

print(f"{len(new_podcasts)} new podcasts found...")

last_youtube_publication_date = get_last_youtube_publication_date()
for podcast in new_podcasts:
    podcast['publication_date'] = last_youtube_publication_date
    last_youtube_publication_date = last_youtube_publication_date + timedelta(days=1)
    # @todo : set hour of publication_date to 6:00AM (with an env variable)

for new_podcast in new_podcasts:
    print(f"Processing {new_podcast.title}...")
    video_path = create_video(new_podcast)
    thumbnail_path = create_thumbnail(video_path, new_podcast)
    upload_video_to_youtube(video_path, thumbnail_path, new_podcast)
    delete_video_and_thumbnail(video_path, thumbnail_path)
    print(f"{new_podcast} processed")

