from langchain_huggingface import HuggingFaceEmbeddings
from typing import List


def get_embeddings(model_name:str) -> 'HuggingFaceEmbeddings':  # "jhgan/ko-sbert-nli"
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
    )
    return embeddings


    