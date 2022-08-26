import feedparser
import ssl
from pprint import pprint
from pathlib import Path



if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

# Création d'une instance
news_feed = feedparser.parse('https://feed.ausha.co/B6Ad3sAApEzX')

def tags_list_flux_rss():
    """Retourne les tags du podcast se trouvant le dossier local "Podcast" """
    for x in Path('Podcast').iterdir():
        s = x.name
    # Propriétés du flux
    tags = []
    for i in news_feed.entries:
        if i['title'] in s:
            pprint(i['title'])
            for z in i['tags']:
                if z['term'] is not None:
                    tags.append(z['term'])
            break
    return tags


def description_flux_rss():
    """Retourne les tags du podcast se trouvant le dossier local "Podcast" """
    for x in Path('Podcast').iterdir():
        s = x.name
    # Propriétés du flux
    for i in news_feed.entries:
        if i['title'] in s:
            description = i['content'][0]['value']
            if "<p>" in description:
                description = description.replace("<p>", "")
            if "</p>" in description:
                description = description.replace("</p>", "")
            break
    return description

if __name__ == '__main__':
    print(description_flux_rss())