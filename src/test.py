import os
from dotenv import load_dotenv

load_dotenv("secrets/.env")

print(type(os.getenv("YT_PLAYLIST_ID")))

