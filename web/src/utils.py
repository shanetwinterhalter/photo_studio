from . import appconfig
from datetime import datetime, timedelta
from os import listdir, path, remove
from time import sleep


def delete_old_files():
    folder_path = appconfig.IMAGE_UPLOADS
    time_limit = datetime.now() - \
        timedelta(hours=appconfig.MAX_IMAGE_AGE_HOURS)
    for filename in listdir(folder_path):
        file_path = path.join(folder_path, filename)

        file_mtime = datetime.fromtimestamp(path.getmtime(file_path))

        if file_mtime < time_limit:
            remove(file_path)
            print(f"Deleted old file: {filename}")
    sleep(3600)
