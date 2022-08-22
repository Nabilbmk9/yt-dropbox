import os
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime
from pathlib import Path
from flux_rss import tags_list_flux_rss, description_flux_rss
from googleapiclient.http import MediaFileUpload
from google_apis import create_service
import socket
socket.setdefaulttimeout(30000)

CLIENT_SECRET_FILE = "code_secret_client_youtube.json"
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
        maxResults=50
    ).execute()
    if 1 > response.get('pageInfo').get('totalResults'):
        return
    else:
        items = response.get('items')
        nextPageToken = response.get('nextPageToken')

        while nextPageToken:
            response_next_page = service.playlistItems().list(
                part='snippet,status',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=nextPageToken
            )
            print(nextPageToken)
            items.extends(response_next_page.get(items))
            nextPageToken = response_next_page.get('nextPageToken')
        return items


def retrieve_status_videos(video_id):
    response = service.videos().list(
        part='snippet,status,liveStreamingDetails',
        id=video_id,
        maxResults=50
    ).execute()
    if 1 > response.get('pageInfo').get('totalResults'):
        return
    else:
        items = response.get('items')
        nextPageToken = response.get('nextPageToken')

        while nextPageToken:
            response_next_page = service.playlistItems().list(
                part='liveStreamingDetails',
                id=video_id,
                maxResults=50,
                pageToken=nextPageToken
            )
            print(nextPageToken)
            items.extends(response_next_page.get(items))
            nextPageToken = response_next_page.get('nextPageToken')
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


if __name__ == '__main__':
    publication_date = datetime(year=2022, month=12, day=26, hour=6)

    telecharger_sur_youtube(publication_date, "titre video", r"C:\Users\boulm\Python_file\MISSION\Youtube_Automation\Output\Visual_Studio_Code_-_connection_api.py_-_Publication_Linkedin_-_Visual_Studio_Code_-_10_March_2022.mp4")
