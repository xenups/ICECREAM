import logging
import mimetypes
import os
import uuid
import rootpath
from ICECREAM.http import HTTPError
from settings import media_path

logger = logging.getLogger()
rootpath.append()


def upload(data, files_key='files', image=True):
    try:
        files = data.get(files_key)
        for file in files:
            # extension = os.path.splitext(file.filename)[1]
            content_type = file.content_type
            extension = mimetypes.guess_extension(content_type)
            if image:
                check_image_extension(extension)
            unique_file_name = str(uuid.uuid4()) + extension
            file.filename = unique_file_name
            save_path = os.path.join(media_path)
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            file.save(save_path)
            return unique_file_name

    except Exception as error:
        raise error


def remove(file_name):
    try:
        path = os.path.join(media_path)
        os.remove(path + file_name)
    except Exception as e:
        logger.error(e)


def check_image_extension(ext):
    if ext not in ('.png', '.jpg', '.jpeg', '.jpe'):
        raise HTTPError(403, "image_type_forbidden")
