from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List


def get_text_spliter(texts: List[str]) -> Document:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 20,     # 청크 사이즈
        chunk_overlap = 10   # 텍스트 겹치는 부분  
    )
    text_document = text_splitter.create_documents(texts)
    return text_document
