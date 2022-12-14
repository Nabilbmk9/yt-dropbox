import os
import feedparser
import ssl
from pprint import pprint
from dotenv import load_dotenv

from helpers import remove_html_tags

load_dotenv(".env")

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

news_feed = feedparser.parse(os.getenv('RSS_FEED_URL'))

def get_tags_and_description_from_rss(podcast_title):   
    for entry in news_feed.entries:
        tags = []
        description = ""
        if podcast_title in entry.title:
            description = entry.summary
            break
    return description, tags 