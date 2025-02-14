import logging


def init_logger(name:str, level:str) -> logging:
    """Logger 생성 함수"""
    logger = logging.getLogger(name=name)
    logger.setLevel(level)

    formatter = logging.Formatter('|%(asctime)s|==|%(name)s||%(levelname)s| %(message)s | %(funcName)s',
                                datefmt='%Y-%m-%d %H:%M:%S'
                                )
    
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger