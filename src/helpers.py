from datetime import datetime, timedelta
from pathlib import Path


def publish_next_day_at_6(from_this_date):
    """Donner une date en argument.
        La fonction va retourner une date qui est le lendemain a 6h"""
    date_de_publication = from_this_date + timedelta(days=1)
    date_de_publication = datetime(date_de_publication.year,
                                   date_de_publication.month,
                                   date_de_publication.day,
                                   date_de_publication.hour - date_de_publication.hour + 6,
                                   date_de_publication.minute - date_de_publication.minute,
                                   date_de_publication.second - date_de_publication.second)
    return date_de_publication


def pending_podcasts(liste_podcast_dropbox, last_youtube_video_posted):
    """Donner en argument, la liste de podcast disponible sur dropbox et la derniere video youtube
        Retourne l'indice du dernier podcast posté sur youtube"""
    if liste_podcast_dropbox is None:
        return 0
    for iterator, nom_podcast in enumerate(liste_podcast_dropbox['name']):
        if last_youtube_video_posted in nom_podcast:
            return iterator
    return iterator +1


def delete_files_in_folder(list_folder):
    for dossier in list_folder:
        for fichier in Path(dossier).iterdir():
            Path(fichier).unlink()


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def from_yt_date_string_to_datetime(yt_date_string):
    """Convert a string to a datetime object"""
    datetime_date = list(yt_date_string)
    datetime_date = "".join(datetime_date[:-1])
    datetime_date = list(datetime_date)
    datetime_date = "".join(datetime_date)
    datetime_date = datetime.fromisoformat(datetime_date)
    return datetime_date


if __name__ == '__main__':
    print(from_yt_date_string_to_datetime("2022-09-20T22:00:00Z"))