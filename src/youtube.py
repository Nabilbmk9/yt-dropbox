import os
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime
from pathlib import Path
from helpers import from_yt_date_string_to_datetime
from rss import *
from googleapiclient.http import MediaFileUpload
from google_apis import create_service
import socket
from pprint import pprint
from dotenv import load_dotenv

load_dotenv(".env")

socket.setdefaulttimeout(30000)

CLIENT_SECRET_FILE = "secrets/code_secret_client_youtube.json"
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
          'https://www.googleapis.com/auth/youtube',
          'https://www.googleapis.com/auth/youtube.force-ssl'
          ]

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def telecharger_sur_youtube(date_de_publication, title_video, chemin_video_a_telecharger):
    """ Télécharge une video sur youtube"""
    service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    upload_date_time = f'{datetime.fromisoformat(str(date_de_publication)).isoformat()}.000Z'

    description = description_flux_rss()

    tags = tags_list_flux_rss()

    request_body = {
        'snippet': {
            'categoryI': 19,
            'title': title_video,
            'description': description,
            'tags': tags
        },
        'status': {
            'privacyStatus': 'private',
            'publishAt': upload_date_time,
            'selfDeclaredMadeForKids': False,
        },
        'notifySubscribers': False
    }

    mediaFile = MediaFileUpload(chemin_video_a_telecharger)

    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()

    service.thumbnails().set(
        videoId=response_upload.get('id'),
        media_body=MediaFileUpload("Thumbnails/thumb.jpg")
    ).execute()


################################################################
# Updated function

def get_latest_video_on_yt(playlist_id):
    response = service.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=1
        ).execute()
    lastest_video = {'title': response['items'][0]['snippet']['title'],
                     'id': response['items'][0]['snippet']['resourceId']['videoId']}
    return lastest_video


def _retrieve_status_video(video_id):
    response = service.videos().list(
        part='snippet,status,liveStreamingDetails',
        id=video_id,
        maxResults=1
    ).execute()
    items = response.get('items')
    return items


def get_last_youtube_publication_date(last_video_id):
    today = datetime.now().replace(microsecond=0)
    publish_at = _retrieve_status_video(last_video_id)[0]['status'].get('publishAt')
    if publish_at is None:
        return today
    publish_at = from_yt_date_string_to_datetime(publish_at)
    return publish_at



if __name__ == '__main__':
    pprint(_retrieve_status_video('EJ2-RCc6bg4'))