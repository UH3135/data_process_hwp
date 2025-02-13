from utils.converter import convert_all_hwp2md
import easyocr
import os

# OCR 모델 로드 (한글 + 영어 지원)
reader = easyocr.Reader(["ko", "en"])

data_path = os.path.abspath("assets/output/acadj_10/bindata/BIN0001.jpg")
# 이미지에서 텍스트 추출
text_results = reader.readtext(data_path)

# 결과 출력
for bbox, text, prob in text_results:
    print(f"텍스트: {text} (정확도: {prob:.2f})")


