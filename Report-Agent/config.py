"""
전역 설정 파일

MOCK_MODE = True 이면 외부 API(Google Sheets, OpenAI, Slack, Email) 없이
로컬 파일과 미리 정의된 응답만으로 전체 파이프라인이 동작합니다.

실제 서비스로 전환하려면:
  1. .env 파일에 API 키를 채워넣고
  2. MOCK_MODE = False 로 변경
  3. src/data_loader.py, report_generator.py, notifier.py 안의
     "실제 연동부"에 표시된 주석을 해제하면 됩니다.
"""

import os

# ---- 데모(포트폴리오) 모드 스위치 ----
MOCK_MODE = True

# ---- 원본 데이터 소스 ----
# 실제 모드에서는 Google Sheets 문서 ID로 교체
GOOGLE_SHEET_ID = os.environ.get("GOOGLE_SHEET_ID", "")
MOCK_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "sample_report_data.csv")

# ---- LLM 설정 ----
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
LLM_MODEL = "gpt-4o-mini"

# ---- 알림 설정 ----
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")
NOTIFY_EMAIL = os.environ.get("NOTIFY_EMAIL", "hr-team@example.com")

# ---- 재시도 정책 ----
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 2

# ---- 경로 ----
BASE_DIR = os.path.dirname(__file__)
LOG_DIR = os.path.join(BASE_DIR, "logs")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
