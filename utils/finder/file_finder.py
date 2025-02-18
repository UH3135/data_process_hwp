import os
from typing import List

from etc.logger import init_logger

logger = init_logger(__file__, 'DEBUG')


def get_filenames_with_type(directory: str, type: str) -> List[str]:
    if not os.path.exists(directory):
        logger.error(f"Error:'{directory}'가 존재하지 않습니다.")
        return []

    files = []
    for root, _, files in os.walk(directory):
        files.extend([os.path.join(root, f) for f in files if f.lower().endswith(f".{type}")])

    if not files:
        logger.error(f"해당 {directory}에 {type} 파일이 없습니다.")
        return []

    logger.info(f"{len(files)}개의 {type} 파일을 찾았습니다.")

    return files

