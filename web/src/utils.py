from . import appconfig
from datetime import datetime, timedelta
from os import listdir, path, remove
from time import sleep


def delete_old_files(folder, time_limit):
    for filename in listdir(folder):
        file_path = path.join(folder, filename)

        file_mtime = datetime.fromtimestamp(path.getmtime(file_path))

        if file_mtime < time_limit:
            remove(file_path)
            print(f"Deleted old file: {filename}")


def cleanup_images():
    img_folders = [appconfig.IMAGE_UPLOADS, appconfig.DEBUG_IMAGE_UPLOADS]
    time_limit = datetime.now() - \
        timedelta(hours=appconfig.MAX_IMAGE_AGE_HOURS)
    for folder in img_folders:
        delete_old_files(folder, time_limit)
    sleep(3600)
