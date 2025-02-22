from bs4 import BeautifulSoup
import markdownify
import re

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


def extract_tables_from_xhtml(file_path, header_orientation="row"):
    """
    XHTML 파일에서 <table> 태그를 추출하여 리스트 형태로 반환하는 함수.
    
    :param file_path: XHTML 파일 경로
    :param header_orientation: "row" 또는 "column", 헤더 방향 설정 (기본: 첫 행을 헤더)
    :return: 표 데이터를 리스트(dict 형태)로 반환
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    soup = BeautifulSoup(content, "xml")
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

def extract_clean_tables_from_markdown(md_text):
    lines = md_text.split("\n")
    tables = []
    current_table = []

    def is_mostly_empty(table):
        """ 
        테이블의 데이터 행이 대부분 비어 있는지 확인 
        - 데이터 행 중 50% 이상이 완전히 비어 있다면 해당 테이블 무시
        """
        if len(table) < 2:  # 헤더만 있는 경우 무시
            return True
        total_rows = len(table) - 1  # 헤더 제외
        empty_rows = sum(1 for row in table[1:] if all(cell == "" for cell in row))  # 완전히 빈 행 수
        return empty_rows / total_rows > 0.5  # 빈 행 비율이 50% 초과하면 제거

    def is_mostly_blank_strings(table):
        """ 
        테이블 전체에서 의미 없는 빈 문자열이 너무 많다면 무시 
        - 전체 셀 중 70% 이상이 빈 문자열이면 해당 테이블 제거 
        """
        total_cells = sum(len(row) for row in table)  # 전체 셀 개수
        empty_cells = sum(cell == "" for row in table for cell in row)  # 빈 문자열 개수
        return empty_cells / total_cells > 0.7  # 빈 셀이 70% 이상이면 무시

    def add_table():
        if current_table:
            # 불필요한 기호 제거
            cleaned_table = [[cell.strip() for cell in row.split("|")[1:-1] if cell.strip() not in ["-", "|"]] 
                             for row in current_table]
            # 빈 행 제거
            cleaned_table = [row for row in cleaned_table if any(cell for cell in row)]
            # 데이터가 대부분 비어있다면 무시
            if len(cleaned_table) > 1 and not is_mostly_empty(cleaned_table) and not is_mostly_blank_strings(cleaned_table):
                tables.append(cleaned_table)
            current_table.clear()

    for line in lines:
        line = line.strip()
        if re.match(r"^\|.*\|$", line):  # 테이블 감지
            current_table.append(line)
        else:
            add_table()  # 테이블 종료

    add_table()  # 마지막 테이블 저장

    return tables