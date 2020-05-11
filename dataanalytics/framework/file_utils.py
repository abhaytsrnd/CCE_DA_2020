import os
import base64
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'csv', 'tsv', 'xlsx', 'xls'}
BASE_PATH = os.path.join('.', 'data')

class FileUtils:

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @staticmethod
    def upload(filename: str, content):
        if FileUtils.allowed_file(filename):
            #File Name & Path
            filename = secure_filename(filename)
            path = FileUtils.path('raw', filename)
            #Basse64 Decode
            key = ';base64,'
            index = content.find(key)
            index = index + len(key)
            content = content[index:]
            content = content.replace(' ', '+')
            data = base64.b64decode(content)
            #Write Data to a file
            with open(path, 'wb') as f:
                f.write(data)

    @staticmethod
    def mkdir(dir: str):
        path = os.path.join(BASE_PATH, dir)
        if not os.path.exists(path):
            os.mkdir(path)

    @staticmethod
    def files(dir: str)-> []:
        path = os.path.join(BASE_PATH, dir)
        files = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                if not file == '.DS_Store':
                    files.append(file)
        return files

    @staticmethod
    def file_format(filename: str) -> str:
        return filename.split('.')[-1]

    @staticmethod
    def append_file_name(filename: str, append: str) -> str:
        name = filename.split('.')[0]
        format = filename.split('.')[-1]
        return name + '-'+ append + '.' + format

    @staticmethod
    def path(dir: str, filename: str):
        path = os.path.join(BASE_PATH, dir)
        path = os.path.join(path, filename)
        return path
