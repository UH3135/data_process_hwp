## 표와 이미지를 오픈소스를 이용해서 파싱하자

### 표

1. File에서 직접 표를 추출
   1. PYMUPDF
   2. pdfplumber
   3. Camelot OCR
2. 이미지로 추출
   1. 이미지로 추출 후 OCR 모델을 이용해서 description을 저장

### 테스트 진행 방법

- 추출한 데이터를 Chroma DB에 저장
- 여러 질문을 토대로 유사한 정답을 추출해서 확인해보기

### 진행상황

1. hwp -> md으로 변환
   1-1. 이미지는 전부 jpg로 저장
2. jpg를 이용하여 OCR 분석

## 사용법
1. assets 파일 생성
   - 아래에 모든 hwp 파일 담아두기 (디렉토리에 담겨있어도 됨)