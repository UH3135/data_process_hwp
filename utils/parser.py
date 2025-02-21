from bs4 import BeautifulSoup
import markdownify
import os

from etc.logger import init_logger

logger = init_logger(__file__, "DEBUG")

class CustomMarkdownConverter(markdownify.MarkdownConverter):
    def convert_img(self, el, text, convert_as_inline):
        src = el.get("src", "").strip()
        alt = el.get("alt", "이미지 없음").strip()

        if not src:
            return ""

        return f"![{alt}]({src})"

def parsing_xhtml(xhtml_path:str, markdown_path:str):
    try:
        with open(xhtml_path, "r", encoding="utf-8") as file:
            xhtml_content = file.read()
        logger.info(f'xhtml load에 성공했습니다.')
    except Exception as e:
        logger.error(f'xhtml load에 실패했습니다. {str(e)}')
        return

    soup = BeautifulSoup(xhtml_content, "xml")
    converter = CustomMarkdownConverter()

    markdown_content = converter.convert_soup(soup)

    try:
        with open(markdown_path, "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)    
        logger.info(f'markdown 파일 생성에 성공했습니다.')
    except Exception as e:
        logger.error(f'markdown 파일 생성에 실패했습니다. {str(e)}')


from bs4 import BeautifulSoup

def extract_tables_from_xhtml(file_path, header_orientation="row"):
    """
    XHTML 파일에서 <table> 태그를 추출하여 리스트 형태로 반환하는 함수.
    
    :param file_path: XHTML 파일 경로
    :param header_orientation: "row" 또는 "column", 헤더 방향 설정 (기본: 첫 행을 헤더)
    :return: 표 데이터를 리스트(dict 형태)로 반환
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    soup = BeautifulSoup(content, "lxml")
    tables = soup.find_all("table")
    extracted_tables = []

    for table in tables:
        table_data = []
        rows = table.find_all("tr")

        # 테이블이 비어 있으면 무시
        if not rows:
            continue

        # 모든 행의 데이터를 리스트 형태로 저장
        matrix = [[td.get_text(strip=True) for td in row.find_all(["th", "td"])] for row in rows]

        # 빈 열 및 빈 행 제거 (완전히 비어 있는 경우)
        matrix = [row for row in matrix if any(cell.strip() for cell in row)]
        matrix = list(map(list, zip(*[col for col in zip(*matrix) if any(cell.strip() for cell in col)])))

        if not matrix:
            continue  # 테이블이 완전히 비어 있으면 무시

        # 헤더 방향에 따른 설정
        if header_orientation == "row":
            headers = matrix[0]  # 첫 행을 헤더로 사용
            data_rows = matrix[1:]
        elif header_orientation == "column":
            headers = [row[0] for row in matrix]  # 첫 열을 헤더로 사용
            data_rows = [row[1:] for row in matrix]
        else:
            raise ValueError("header_orientation은 'row' 또는 'column'이어야 합니다.")

        # JSON 변환을 위해 딕셔너리로 변환
        table_dicts = [dict(zip(headers, row)) for row in data_rows if len(row) == len(headers)]
        extracted_tables.append(table_dicts)

    return extracted_tables

