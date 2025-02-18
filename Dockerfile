# 베이스 이미지 선택
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# 애플리케이션 실행
CMD ["python", "main.py"]