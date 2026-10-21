"""
설정 파일
- 구글 API 인증정보, 이메일 계정 정보 등 민감한 값은
  .env 파일 또는 환경변수로 분리하여 관리한다.
- 실제 값은 .env.example을 복사한 .env 파일에 채워 넣는다.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# --- Google Sheets ---
GOOGLE_SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service_account.json")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "")          # 구글 시트 URL의 /d/ 뒤 ID
SHEET_NAME = os.getenv("SHEET_NAME", "시트1")

# --- Google Calendar (2단계 확장용) ---
CALENDAR_ID = os.getenv("CALENDAR_ID", "primary")

# --- Email (SMTP) ---
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_APP_PASSWORD = os.getenv("SMTP_APP_PASSWORD", "")     # 구글 앱 비밀번호
ALERT_RECEIVER = os.getenv("ALERT_RECEIVER", SMTP_USERNAME)

# --- 알림 조건 ---
ALERT_DAYS_BEFORE = [3, 1]   # D-3, D-1 알림
