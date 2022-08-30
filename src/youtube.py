import os
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime
from pathlib import Path
from rss import tags_list_flux_rss, description_flux_rss
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


def get_channel_info():
    response = service.channels().list(
        mine=True,
        part='contentDetails'
    ).execute()
    return response


channel_response = get_channel_info()
uploaded_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']


def retrieve_playlist_videos(playlist_id):
    response = service.playlistItems().list(
        part='snippet,status',
        playlistId=playlist_id,
        maxResults=1
        ).execute()

    return response.get('items')


def retrieve_status_videos(video_id):
    response = service.videos().list(
        part='snippet,status,liveStreamingDetails',
        id=video_id,
        maxResults=50
    ).execute()
    items = response.get('items')
    return items


def retrieve_lastest_title_and_date_video():
    today = datetime.now().replace(microsecond=0)
    videos = retrieve_playlist_videos(uploaded_playlist_id)

    for video_infos in videos:
        videoId = video_infos['snippet']['resourceId']['videoId']
        title_video = retrieve_status_videos(videoId)[0]['snippet'].get('title')
        publish_at = retrieve_status_videos(videoId)[0]['status'].get('publishAt')
        if publish_at is None:
            return title_video, today
        publish_at = list(publish_at)
        publish_at = "".join(publish_at[:-1])
        publish_at = list(publish_at)
        publish_at = "".join(publish_at)
        publish_at = datetime.fromisoformat(publish_at)
        break
    return title_video, publish_at

################################################################
# NEWS FUNCTIONS
def get_latest_video_on_yt(playlist_id):
    response = service.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=1
        ).execute()
    lastest_video = {'title': response['items'][0]['snippet']['title'],
                     'id': response['items'][0]['snippet']['resourceId']['videoId']}
    return lastest_video    
    

if __name__ == '__main__':
    pprint(get_latest_video_on_yt(os.getenv("YT_PLAYLIST_ID"))['title'])