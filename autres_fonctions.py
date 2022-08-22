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


def pending_podcasts(liste_podact_dropbox, last_youtube_video_posted):
    """Donner en argument, la liste de podcast disponible sur dropbox et la derniere video youtube
        Retourne l'indice du dernier podcast posté sur youtube"""
    for indice, x in enumerate(liste_podact_dropbox['name']):
        if last_youtube_video_posted in x:
            return indice
    return None


def delete_files_in_folder(list_folder):
    for dossier in list_folder:
        for fichier in Path(dossier).iterdir():
            Path(fichier).unlink()