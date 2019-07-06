import os,io
from zipfile import ZipFile 
from os import path


class Utils:
    @staticmethod
    def make_zip_file_bytes(path):
        buf = io.BytesIO()
        with ZipFile(buf, 'w') as z:
            for full_path,archive_name in Utils.files_to_zip(path=path):
                z.write(full_path, archive_name)
        return buf.getvalue()



    @staticmethod
    def files_to_zip(path):
        for root, dirs, files in os.walk(path):
            for f in files:
                full_path = os.path.join(root, f)
                archive_name = full_path[len(path) + len(os.sep):]
                yield full_path, archive_name



source_folder='python_lambda'
folder_path = path.join(path.dirname(path.abspath(__file__)), source_folder)
print(folder_path)
zip_file=Utils.make_zip_file_bytes(path=folder_path)
print(zip_file)

