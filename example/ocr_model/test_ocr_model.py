import os
from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
from dotenv import load_dotenv

# from utils.ocr_models import md2txt_with_ocr
load_dotenv()

TEST_MD_PATH = os.path.abspath("assets/output/acadj_10/acadj_10.md")
TEST_PDF_PATH = os.path.abspath("/mnt/e/WSL/home/uihyun/data_process_hwp/assets/전자기학(전기자기학)통합과정_백주기/elmabjk_22.pdf")

