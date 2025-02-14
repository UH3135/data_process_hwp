from utils.finder import get_hwp_filenames
from utils.converter.converter import hwp_to_md, hwp_to_pdf

def convert_all_hwp2md(data_path:str):
    for file_path in get_hwp_filenames(data_path):
        hwp_to_md(file_path)


def convert_all_hwp2pdf(data_path:str):
    for file_path in get_hwp_filenames(data_path):
        hwp_to_pdf(file_path)