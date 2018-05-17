import os

class File_Location:

    def get_csv_file(self, file_dir):
        file_path = file_dir

        for file in os.listdir(file_dir):
            if file.endswith('.csv'):
                return file_path + file
        return file_path

    def get_xls_file(self, file_dir):
        for file in os.listdir(file_dir):
            if file.endswith('.xls'):
                return file_dir + '/' + file
        return file_dir