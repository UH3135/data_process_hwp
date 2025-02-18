from langchain_core.prompts import ChatPromptTemplate


rag_prompt = ChatPromptTemplate.from_template(
        """
        당신은 주어진 문서를 바탕으로 질문에 답하는 AI입니다.  
        아래는 참조할 문서입니다:  

        {context}  

        사용자의 질문: "{question}"  

        위의 문서를 참고하여 명확하고 정확한 답변을 제공하세요.  
        만약 문서에 관련 정보가 없으면 "제공된 문서에서 해당 정보를 찾을 수 없습니다."라고 답변하세요.  
        """
)