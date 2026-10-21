"""
원본 데이터 수집 모듈

목업 모드: 로컬 CSV(data/sample_report_data.csv)를 읽음
실제 모드: Google Sheets API로 원본 시트를 읽음 (아래 함수 내 주석 참고)
"""

import csv
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import config


def load_source_data():
    if config.MOCK_MODE:
        return _load_from_csv(config.MOCK_DATA_PATH)
    else:
        return _load_from_google_sheets(config.GOOGLE_SHEET_ID)


def _load_from_csv(path):
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]
    return rows


def _load_from_google_sheets(sheet_id):
    """
    실제 연동부 (MOCK_MODE = False 일 때 사용)

    pip install gspread google-auth 필요, 서비스 계정 JSON 키 발급 후 사용

    import gspread
    gc = gspread.service_account(filename="service_account.json")
    sh = gc.open_by_key(sheet_id)
    worksheet = sh.sheet1
    return worksheet.get_all_records()
    """
    raise NotImplementedError(
        "실제 Google Sheets 연동은 MOCK_MODE=False 설정 후 "
        "서비스 계정 키를 발급받아 위 주석의 코드를 활성화하세요."
    )
