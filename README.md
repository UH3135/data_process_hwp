## 표와 이미지를 오픈소스를 이용해서 파싱하자

### 표

1. File에서 직접 표를 추출
   1. PYMUPDF
   2. pdfplumber
   3. Camelot OCR
2. 이미지로 추출
   1. 이미지로 추출 후 OCR 모델을 이용해서 description을 저장
      - easy_ocr
      - Azure document ai -> 유료지만 학생 $100 혜택이 존재
   2. 수식 데이터는 LaTeX 데이터로 변환
3. 영상 데이터
   1. 음성은 wav 파일로 추출

### 테스트 진행 방법

- 추출한 데이터를 Chroma DB에 저장
- ollama + deepseek 15B 모델로 RAG 구축

### 진행상황

1. hwp to md+html으로 변환
   1-1. 이미지는 전부 jpg로 저장
2. jpg를 이용하여 OCR 분석
   2-1. easy ocr, azure ai 두개 테스트 완료
3. hwp to pdf 변환

## 사용법
1. assets 파일 생성
   - 아래에 모든 hwp 파일 담아두기 (디렉토리에 담겨있어도 됨)