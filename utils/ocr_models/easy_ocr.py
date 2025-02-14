import easyocr
import os


def easy_ocr(file_path: str):
    reader = easyocr.Reader(["ko", "en"])

    data_path = os.path.abspath(file_path)
    text_results = reader.readtext(data_path)

    for bbox, text, prob in text_results:
        print(f"텍스트: {text} (정확도: {prob:.2f})")

