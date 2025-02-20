## 표와 이미지를 오픈소스를 이용해서 파싱

### Hwp to Json

1. HWP의 경우
   1. Pyhwp을 사용해서 hwp -> markdown으로 변환
   2. markdown에서 JPG를 OCR 모델에 보내서 Text로 변환
      2-1. 변환된 Text는 Markdown에 추가
      2-2. TODO: OCR 모델 선정 (임시로 Azure Document AI로 사용)
   3. 모두 Text로 되어있는 Markdown을 JSON 객체로 변환
      3-1. 수식은 어떻게 저장할 것인지
2. PDF의 경우
   1. OCR 모델을 이용해서 바로 Text로 변환
   2. 수식 데이터는 LaTeX 데이터로 변환

### 영상 데이터
   1. Mp4 파일을 wav 파일로 추출

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
