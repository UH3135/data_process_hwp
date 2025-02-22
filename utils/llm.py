from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import json
import os
import re

from etc.logger import init_logger

logger = init_logger(__file__, "DEBUG")

# 환경 변수 로드
load_dotenv()

api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")


def extract_tables_from_text(text):
    messages = [
        {"role": "system", "content": """
            아래 문서에서 테이블 데이터를 JSON으로 변환해주세요. JSON 형식은 다음과 같이 유지되어야 합니다:
            {
                "tables": [
                    {
                        "name": "테이블 제목",
                        "headers": ["열 제목1", "열 제목2", "열 제목3"],
                        "rows": [
                            ["값1", "값2", "값3"],
                            ["값4", "값5", "값6"]
                        ]
                    }
                ]
            }
            JSON 형식 이외의 불필요한 설명은 포함하지 말고 순수한 JSON 데이터만 출력하세요.
        """},
        {"role": "user", "content": f"""
            === 원본 텍스트 ===
            {text}
            ==================
            위 마크다운 문서에서 모든 테이블을 JSON으로 변환해줘.
        """}
    ]

    # LangChain OpenAI 모델 설정
    # llm = ChatOpenAI(
    #     model_name="gpt-4o",  
    #     openai_api_key=os.getenv("OPENAI_API_KEY"),
    #     temperature=0
    # )

    llm = ChatOllama(model="jung/bllossom")

    ai_msg = llm.invoke(messages)
    response_content = ai_msg.content if hasattr(ai_msg, "content") else ai_msg
    if not response_content:
        logger.error("답변을 받지 못했습니다.")
    logger.info(response_content)

    json_pattern = r"```json\n(.*?)\n```"
    match = re.search(json_pattern, response_content, re.DOTALL)

    if match:
        json_content = match.group(1)
        with open('output.json', 'w', encoding='utf-8') as f:
            f.write(json_content)
        print("JSON 부분이 'output.json' 파일에 저장되었습니다.")
    else:
        print("JSON 부분을 찾을 수 없습니다.")

    return json_content


def translate_with_llm(text:str) -> str:
    translate_llm = ChatOllama(model="hf.co/teddylee777/Llama-3-Open-Ko-8B-gguf:Q4_0")
