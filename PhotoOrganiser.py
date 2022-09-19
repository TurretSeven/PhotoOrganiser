
import shutil
import os
import json
import sys
from exiftool import ExifToolHelper
from pathlib import Path


# noinspection PyBroadException
def get_ymd(file_path: str) -> tuple:
    """
        Get the year, month and day the photo was taken

        :return: Year, Month and Day values as a tuple.
    """
    image_date = []
    date_created = "0:0:0"

    try:
        with ExifToolHelper() as et:
            meta_data = et.get_tags([file_path], tags=["EXIF:DateTimeOriginal"])

        if len(meta_data) == 1:
            date_time_original = meta_data[0]["EXIF:DateTimeOriginal"]

            if ":" in date_time_original:
                date_created = date_time_original[:10]
    except IndexError:
        print(f"An exception has been raised on [{file_path}].")
    finally:
        image_date = date_created.split(':')

        return image_date[0], image_date[1], image_date[2]


def read_config() -> dict:
    """
        Read in paths from json file

        :return: List containing source and destination folder paths
    """
    config_file = open("PhotoOrganiser.json", "rt")
    path_list = json.loads(config_file.read())

    return path_list


def copy_files (root_source, root_destination):
    """
        Create the destination folder and copy the image files.
    """

    file_ext = (".tif", "jpg", "jpeg")

    for dir_name, sub_dir_list, file_list in os.walk(root_source):
        for fname in file_list:
            if ".@__thumb" not in dir_name:
                if ".DS_Store" not in fname and (fname.casefold().endswith(file_ext)):
                    source_file_path = os.path.join(dir_name, fname)

                    # Read the date created/taken from the file
                    print(f'\nReading: {source_file_path}')
                    ymd = get_ymd(source_file_path)

                    # Create destination folder
                    destination_folder = os.path.join(root_destination, ymd[0], ymd[1], ymd[2])
                    Path(destination_folder).mkdir(parents=True, exist_ok=True)

                    # Copy file
                    print(f'Copying: {destination_folder}/{fname}')
                    shutil.copy2(source_file_path, destination_folder)

    return None


def main():
    """ Run as program """

    # Read the config file
    path_list = read_config()

    # Get the starting root directory
    root_dir = path_list['SourcePath']
    print(root_dir)

    copy_files(root_dir, path_list['DestinationPath'])
    return None


if __name__ == "__main__":
    main()
    sys.exit(0)
