import feedparser
import ssl
from pprint import pprint
from pathlib import Path



if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

news_feed = feedparser.parse('https://feed.ausha.co/B6Ad3sAApEzX')

def get_description_from_rss(podcast_title):
    for meditation_podcast in news_feed.entries:
        if podcast_title in meditation_podcast['title']:
            description = meditation_podcast['content'][0]['value']
            if "<p>" in description:
                description = description.replace("<p>", "")
            if "</p>" in description:
                description = description.replace("</p>", "")
            break
    return description


def get_tags_from_rss(podcast_title):
    tags = []
    for meditation_podcast in news_feed.entries:
        if podcast_title in meditation_podcast['title']:
            for tag in meditation_podcast['tags']:
                if tag['term'] is not None:
                    tags.append(tag['term'])
            break
    return tags


if __name__ == '__main__':
    pprint(get_tags_from_rss("13 minutes pour se détendre sur une plage (vous êtes au bon endroit)"))