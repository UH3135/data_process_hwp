from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
import os

OCRLoader = AzureAIDocumentIntelligenceLoader(
    api_endpoint=os.getenv("AZURE_COGNITIVE_API_ENDPOINT"), 
    api_key=os.getenv("AZURE_COGNITIVE_API_KEY"),  
    api_model="prebuilt-layout",
    file_path=file_path,
    mode="page"
)

documents = OCRLoader.load()