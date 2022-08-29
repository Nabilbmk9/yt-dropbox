import time, random, os
from datetime import datetime
from pathlib import Path
import moviepy.editor as me

from src.rss import *
from src.dropbox import *
from src.videos import *
from src.youtube import *
from src.helpers import *
from src.helpers import *

latest_video_title = get_latest_video_on_yt() # -> "The latest video on youtube"

podcasts_path = os.environ.get("PODCASTS_PATH") # -> "/Podcast"
new_podcasts = get_new_podcasts(podcasts_path, latest_video_title)
# -> new_podcasts = [{title: "Title", description: "", path: "/Podcast/title.mp3", tags: ["paix", "amour"], publication_date: ""}, {}, {}]

for podcast in new_podcasts:
    podcast['description'] = get_description_from_rss(podcast['title']) 

if new_podcasts == []:
    print("No new podcast")
    exit()

print(f"{new_podcasts.lenght} new podcasts found...")

last_youtube_publication_date = get_last_youtube_publication_date()
for podcast in new_podcasts:
    podcast['publication_date'] = last_youtube_publication_date
    last_youtube_publication_date = last_youtube_publication_date + datetime.timedelta(days=1)
    # @todo : set hour of publication_date to 6:00AM (with an env variable)

for new_podcast in new_podcasts:
    print(f"Processing {new_podcast.title}...")
    video_path = create_video(new_podcast)
    thumbnail_path = create_thumbnail(video_path, new_podcast)
    upload_video_to_youtube(video_path, thumbnail_path, new_podcast)
    delete_video_and_thumbnail(video_path, thumbnail_path)
    print(f"{new_podcast} processed")
