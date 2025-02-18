from langchain_core.documents import Document
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import Chroma
from kiwipiepy import Kiwi
from typing import List


def kiwi_toknize(text):
    kiwi = Kiwi()
    return [token.form for token in kiwi.tokenize(text)]


def get_em25_retriever(text_document: List[Document], k) -> 'BM25Retriever':
    bm25_retriever = BM25Retriever.from_documents(
        documents=text_document,
        process_func=kiwi_toknize,
    )
    bm25_retriever.k = k
    return bm25_retriever


def get_db_retriever(text_document: List[Document], embeddings, k):
    db = Chroma.from_documents(
        documents=text_document,
        embedding=embeddings
    )
    db_retriever = db.as_retriever(search_kwargs={'k':k})
    return db_retriever


def get_ensemble_retriever(text_document: List[Document], embeddings, k=20):  # k는 반환할 문서 수
    em25 = get_em25_retriever(text_document, k)
    db = get_db_retriever(text_document, embeddings, k)
    ensemble_retriever = EnsembleRetriever(                         # 리트리버 앙상블 
        retrievers = [em25, db], weights = [0.5, 0.5]
    )
    return ensemble_retriever
