import os
import feedparser
import ssl
from pprint import pprint
from pathlib import Path
from dotenv import load_dotenv

from helpers import remove_html_tags

load_dotenv(".env")


if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

news_feed = feedparser.parse(os.getenv('RSS_FEED_URL'))

def get_tags_and_description_from_rss(podcast_title):
    tags = []
    for entry in news_feed.entries:
        if podcast_title in entry['title']:
            description = entry['content'][0]['value']
            description = remove_html_tags(description)
            tags.extend(tag['term'] for tag in entry['tags'] if tag['term'] is not None)
            break
    return description, tags


if __name__ == '__main__':
    pprint(get_tags_and_description_from_rss("13 minutes pour se détendre sur une plage (vous êtes au bon endroit)"))