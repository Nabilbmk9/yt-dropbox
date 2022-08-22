import pathlib
import pandas as pd
import dropbox
from dropbox.exceptions import AuthError

DROPBOX_ACCESS_TOKEN = 'sl.BMRT-az24gqH0hvucQT7Cq3Qm4HWSaB3QBhLtqX_VjSiLq64jSzx7HIwh1gBG5Q2RwuqcdYzV6D76kCQqn8OVq20JC8jqjukxrwbksCahTnYCZkOU58SJgDcDtb5DgEdmXWCHQ8'

BASE_DIR = pathlib.Path().cwd()


def dropbox_connect():
    """Create a connection to Dropbox."""
    try:
        dbx = dropbox.Dropbox(app_key="17k9km7m0o1xvbp",
                              app_secret="lif05vsdr7wdplt",
                              oauth2_refresh_token="_8sOiO88uLcAAAAAAAAAAcorNALS5NwU51pKjtpdTmqY308mboD05lcLbVGAkeEM")
    except AuthError as e:
        print(f'Error connecting to Dropbox with access token: {str(e)}')
    return dbx


def dropbox_list_files(podcast_path): # example podcast_path -> "/Podcast"
    """Return a Pandas dataframe of files in a given Dropbox folder path in the Apps directory."""

    dbx = dropbox_connect()

    try:
        files = dbx.files_list_folder(podcast_path).entries
        files_list = []
        for file in files:
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


def dropbox_download_file(dropbox_file_path, local_file_path):
    """Download a file from Dropbox to the local machine."""

    try:
        dbx = dropbox_connect()
        with open(local_file_path, 'wb') as f:
            metadata, result = dbx.files_download(path=dropbox_file_path)
            f.write(result.content)
    except Exception as e:
        print(f'Error downloading file from Dropbox: {str(e)}')


if __name__ == '__main__':
    print(dropbox_list_files("/Podcast"))