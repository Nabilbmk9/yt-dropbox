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

def get_description_from_rss(podcast_title):
    for entry in news_feed.entries:
        if podcast_title in entry['title']:
            description = entry['content'][0]['value']
            description = remove_html_tags(description)
            break
    return description


def get_tags_from_rss(podcast_title):
    tags = []
    for entry in news_feed.entries:
        if podcast_title in entry['title']:
            for tag in entry['tags']:
                if tag['term'] is not None:
                    tags.append(tag['term'])
            break
    return tags


if __name__ == '__main__':
    pprint(get_description_from_rss("13 minutes pour se détendre sur une plage (vous êtes au bon endroit)"))