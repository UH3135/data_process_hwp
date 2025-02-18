from langchain_core.documents import Document
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from typing import List

from ai_model.prompt import rag_prompt
from ai_model.retriever import get_ensemble_retriever
from ai_model.embedding import get_embeddings


def get_answer_llm(query:str, documents: List[Document]):
    embedding = get_embeddings("jhgan/ko-sbert-nli")
    retriever = get_ensemble_retriever(text_document=documents, embeddings=embedding, k=3)
    llm = ChatOllama(model="deepseek-r1:8b")

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    response = chain.invoke(query)
    return response