import os
import pathlib
import pandas as pd
import dropbox
from dropbox.exceptions import AuthError
from dotenv import load_dotenv
from pprint import pprint

load_dotenv(".env")

BASE_DIR = pathlib.Path().cwd()


def _dropbox_connect():
    """Create a connection to Dropbox."""
    try:
        dbx = dropbox.Dropbox(app_key=os.environ.get("APP_KEY"),
                              app_secret=os.environ.get("APP_SECRET"),
                              oauth2_refresh_token=os.environ.get("OAUTH2_REFRESH_TOKEN"))
    except AuthError as e:
        print(f'Error connecting to Dropbox with access token: {str(e)}')
    return dbx


def _dropbox_list_files(folder_path): # example podcast_path -> "/Podcast"
    """Return a Pandas dataframe of files in a given Dropbox folder path in the Apps directory."""
    dbx = _dropbox_connect()
    files_list = []
    try:
        files_list_folder = dbx.files_list_folder(folder_path)
        for file in files_list_folder.entries:
            if isinstance(file, dropbox.files.FileMetadata):
                metadata = {
                    'name': file.name,
                    'path_display': file.path_display,
                    'client_modified': file.client_modified,
                    'server_modified': file.server_modified
                }
                files_list.append(metadata)
        
        while files_list_folder.has_more:
            files_list_folder = dbx.files_list_folder_continue(files_list_folder.cursor)
            for file in files_list_folder.entries:
                if isinstance(file, dropbox.files.FileMetadata):
                    metadata = {
                        'name': file.name,
                        'path_display': file.path_display,
                        'client_modified': file.client_modified,
                        'server_modified': file.server_modified
                    }
                    files_list.append(metadata)

        df = pd.DataFrame.from_records(files_list)
        return df.sort_values(by='name', ascending=False)

    except Exception as e:
        print(f'Error getting list of files from Dropbox: {str(e)}')


def _dropbox_download_file(dropbox_file_path, local_file_path):
    """Download a file from Dropbox to the local machine."""
    try:
        dbx = _dropbox_connect()
        with open(local_file_path, 'wb') as f:
            metadata, result = dbx.files_download(path=dropbox_file_path)
            f.write(result.content)
    except Exception as e:
        print(f'Error downloading file from Dropbox: {str(e)}')


def get_new_podcasts(podcasts_path, latest_video_title):
    all_podcasts = _dropbox_list_files(podcasts_path)
    if all_podcasts is None:
        return []
    all_podcasts = all_podcasts[all_podcasts['name'].str.endswith('.mp3')]
    
    new_podcasts = []
    for podcast_name, podcast_path in zip(all_podcasts['name'], all_podcasts['path_display']):
        if latest_video_title in podcast_name:
            return new_podcasts
        new_podcasts.append({'title': podcast_name.split(" - ", 1)[1].split(".", 1)[0], 'path': podcast_path})
    
    return new_podcasts
