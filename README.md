## 표와 이미지를 오픈소스를 이용해서 파싱

### 표

1. File에서 직접 표를 추출
   1. PYMUPDF
   2. pdfplumber
2. 이미지로 추출
   1. 이미지로 추출 후 OCR 모델을 이용해서 description을 저장
      - easy_ocr
      - Azure document ai -> 유료지만 학생 $100 혜택이 존재
   2. 수식 데이터는 LaTeX 데이터로 변환
3. 영상 데이터
   1. 음성은 wav 파일로 추출

## 사용법

1. hwp5 패키지 설치
   1-1. hwp5를 위한 패키지 설치
   ```
   sudo apt update
   sudo apt install build-essential cmake libxml2-dev libxslt1-dev
   ```

   1-2. hwp5 설치
   ```
   pip install --pre pyhwp
   ```

2. assets 파일 생성
   - 아래에 모든 hwp 파일 담아두기 (디렉토리에 담겨있어도 됨)

3. azure api key 설정
   - .env 파일 작성 (root)
   ```
   AZURE_COGNITIVE_API_ENDPOINT=your_endpoint
   AZURE_COGNITIVE_API_KEY=your_api_key

   ```

4. python 실행
   ```
   python main.py
   ```

## 유의사항

1. mac or Linux 계열의 경우 pywin32는 사용하지 못함: Hwp to pdf 코드 사용불가
2. python 3.11 버전 지원
