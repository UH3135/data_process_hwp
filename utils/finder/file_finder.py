import os

from etc.logger import init_logger

logger = init_logger(__file__, 'DEBUG')


def get_hwp_filenames(directory):
    if not os.path.exists(directory):
        logger.error(f"Error:'{directory}'가 존재하지 않습니다.")
        return []

    hwp_files = []
    for root, _, files in os.walk(directory):
        hwp_files.extend([os.path.join(root, f) for f in files if f.lower().endswith(".hwp")])

    if not hwp_files:
        logger.error(f"해당 {directory}에 HWP 파일이 없습니다.")
        return []

    logger.info(f"{len(hwp_files)}개의 HWP 파일을 찾았습니다.")

    return hwp_files


def get_jpg_filenames(directory):
    if not os.path.exists(directory):
        logger.error(f"Error:'{directory}'가 존재하지 않습니다.")
        return []

    hwp_files = []
    for root, _, files in os.walk(directory):
        hwp_files.extend([os.path.join(root, f) for f in files if f.lower().endswith(".jpg")])

    if not hwp_files:
        logger.error(f"해당 {directory}에 jpg 파일이 없습니다.")
        return []

    logger.info(f"{len(hwp_files)}개의 jpg 파일을 찾았습니다.")

    return hwp_files

def get_mp4_filenames(directory):
    if not os.path.exists(directory):
        logger.error(f"Error:'{directory}'가 존재하지 않습니다.")
        return []

    hwp_files = []
    for root, _, files in os.walk(directory):
        hwp_files.extend([os.path.join(root, f) for f in files if f.lower().endswith(".mp4")])

    if not hwp_files:
        logger.error(f"해당 {directory}에 mp4 파일이 없습니다.")
        return []

    logger.info(f"{len(hwp_files)}개의 mp4 파일을 찾았습니다.")

    return hwp_files
