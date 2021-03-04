from os import path
from io import TextIOWrapper
from src.utils.files_read_mode import FileReadMode


class FileHandler:
    def read_file(self, relative_path: str, read_mode: str) -> TextIOWrapper:
        """Return a file based on project folder
        read_file(relative_path: str)
        :param relative_path: relative path of file starting at folder project
        :type relative_path: _io.TextIOWrapper
        """
        try:
            return open(self.path_generator(relative_path), read_mode)
        except FileNotFoundError as err:
            print(err)
    
    def path_generator(self, relative_path: str) -> str:
        """Return a path of file based on project folder
        path_generator(relative_path: str)
        :param relative_path: relative path of file starting at folder project
        """
        return path.join(path.abspath(''), relative_path)
