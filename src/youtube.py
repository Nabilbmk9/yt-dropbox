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

from thumbnail import create_thumbnail

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


def upload_video_to_youtube(video_info, video_path, thumbnail_path):
    service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    title_video = video_info['title']
    upload_date_time = video_info['publication_date']
    description = video_info['description']
    tags = video_info['tags']

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

    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=MediaFileUpload(video_path)
    ).execute()

    service.thumbnails().set(
        videoId=response_upload.get('id'),
        media_body=MediaFileUpload(thumbnail_path)
    ).execute()


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
