import json
import re

import re

# Markdown 파일 경로
md_file_path = "/mnt/data/과업지시서_v1.0.md"

# Markdown을 전처리하여 깨끗한 텍스트로 변환하는 함수
def preprocess_markdown(md_text):
    lines = md_text.split("\n")
    processed_text = []
    current_page = []
    
    def add_page():
        """현재 페이지 내용을 저장하고 페이지 구분을 추가"""
        if current_page:
            processed_text.append("  ".join(current_page))  # 페이지 단위로 스페이스 두 번 추가
            current_page.clear()

    for line in lines:
        line = line.strip()

        # 불필요한 기호 및 공백 제거
        line = re.sub(r"\s+", " ", line)  # 연속된 공백을 하나로
        line = re.sub(r"[-—]+", "", line)  # 불필요한 구분선 제거
        line = re.sub(r"\|", "", line)  # 표 구분 기호 제거
        line = re.sub(r"^\d+\.$", "", line)  # 단순 숫자(번호) 제거

        # 의미 없는 빈 줄 제거
        if line and not re.match(r"^\s*$", line):
            if re.match(r"^[ⅠⅡⅢⅣⅤ]+", line):  # 제목이 포함된 경우 페이지 단위로 추가
                add_page()
            current_page.append(line)

    add_page()  # 마지막 페이지 추가

    return "\n".join(processed_text)  # 최종 결과 반환
