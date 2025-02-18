from utils.converter.converter import hwp_to_md
from utils.finder import get_filenames_with_type


def convert_all_hwp2md(data_path:str):
    for file_path in get_filenames_with_type(data_path, 'hwp'):
        hwp_to_md(file_path)
