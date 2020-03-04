import os
import uuid
import rootpath
from settings import media_path

rootpath.append()


def upload(data, files_key='files'):
    try:
        files = data.get(files_key)
        for file in files:
            extension = os.path.splitext(file.filename)[1]
            unique_file_name = str(uuid.uuid4()) + extension
            file.filename = unique_file_name
            save_path = os.path.join(media_path)
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            file.save(save_path)
            return unique_file_name

    except Exception as error:
        print(error)
        raise error
