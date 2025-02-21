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
        logger.info(f'xhtml load에 성공했습니다. {xhtml_path}')
    except Exception as e:
        logger.error(f'xhtml load에 실패했습니다. {str(e)}')
        return

    soup = BeautifulSoup(xhtml_content, "xml")
    converter = CustomMarkdownConverter()

    markdown_content = converter.convert_soup(soup)

    try:
        with open(markdown_path, "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)    
        logger.info(f'markdown 파일 생성에 성공했습니다. {markdown_path}')
    except Exception as e:
        logger.error(f'markdown 파일 생성에 실패했습니다. {str(e)}')
