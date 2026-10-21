"""
구글 시트에서 정산 항목(항목명·담당자·마감일·알림상태)을 읽어오는 모듈.

두 가지 모드를 지원한다.
- mock 모드: API 키 없이 data/sample_deadlines.csv 파일을 읽어 테스트
- live 모드: 실제 구글 서비스 계정 인증으로 구글 시트를 읽음 (API 키 준비 후 사용)
"""

import csv
import os
from dataclasses import dataclass
from datetime import date, datetime

import config


@dataclass
class DeadlineItem:
    name: str          # 항목명
    owner: str          # 담당자
    due_date: date       # 마감일
    notified: str        # 알림상태 (기존에 알림을 보냈는지 기록)


def _parse_date(value: str) -> date:
    return datetime.strptime(value.strip(), "%Y-%m-%d").date()


def read_from_csv(path: str) -> list[DeadlineItem]:
    """로컬 CSV 파일에서 항목을 읽는다 (테스트용)."""
    items = []
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append(
                DeadlineItem(
                    name=row["항목명"].strip(),
                    owner=row["담당자"].strip(),
                    due_date=_parse_date(row["마감일"]),
                    notified=row.get("알림상태", "").strip(),
                )
            )
    return items


def read_from_google_sheet() -> list[DeadlineItem]:
    """실제 구글 시트에서 항목을 읽는다 (서비스 계정 키 준비 후 사용)."""
    import gspread
    from google.oauth2.service_account import Credentials

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(
        config.GOOGLE_SERVICE_ACCOUNT_FILE, scopes=scopes
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(config.SPREADSHEET_ID).worksheet(config.SHEET_NAME)
    rows = sheet.get_all_records()  # 첫 행을 헤더로 사용

    items = []
    for row in rows:
        if not row.get("항목명") or not row.get("마감일"):
            continue
        items.append(
            DeadlineItem(
                name=str(row["항목명"]).strip(),
                owner=str(row.get("담당자", "")).strip(),
                due_date=_parse_date(str(row["마감일"])),
                notified=str(row.get("알림상태", "")).strip(),
            )
        )
    return items


def get_items(mock: bool = True) -> list[DeadlineItem]:
    if mock:
        sample_path = os.path.join(os.path.dirname(__file__), "data", "sample_deadlines.csv")
        return read_from_csv(sample_path)
    return read_from_google_sheet()
