def extract_tables(md_lines):
    """Markdown 문서에서 테이블을 추출"""
    tables = []
    table = []
    in_table = False

    for line in md_lines:
        # 테이블 시작 감지 (|로 시작하는 줄)
        if line.strip().startswith("|"):
            in_table = True
            table.append(line.strip())
        elif in_table:
            # 테이블 종료 감지 (공백 줄)
            tables.append(table)
            table = []
            in_table = False

    return tables