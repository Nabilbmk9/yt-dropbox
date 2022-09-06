from datetime import datetime, timedelta
from pathlib import Path


def publish_time(publication_date, post_time_hour=6, post_time_minute=0):
    publication_date = datetime(publication_date.year,
                                   publication_date.month,
                                   publication_date.day,
                                   publication_date.hour - publication_date.hour + post_time_hour,
                                   publication_date.minute - publication_date.minute + post_time_minute,
                                   publication_date.second - publication_date.second)
    return publication_date


def delete_tmp_files():
    list_folders = ["tmp/Podcast", "tmp/Videos", "tmp/Thumbnail", "tmp/Output"]
    for dossier in list_folders:
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


def yt_format_date(datetime_object):
    """Convert a datetime object to a youtube string format"""
    return f'{datetime.fromisoformat(str(datetime_object)).isoformat()}.000Z'

if __name__ == '__main__':
    delete_tmp_files()