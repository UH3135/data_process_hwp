import easyocr

from etc.logger import init_logger


def get_easy_ocr(data_path:str):
    reader = easyocr.Reader(["ko", "en"])
    text_results = reader.readtext(data_path)
    result = []
    for _, text, _ in text_results:
        result.append(str(text))

    return "\n".join(result)
