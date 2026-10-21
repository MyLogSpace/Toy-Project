"""
정산 마감 알리미 - 메인 실행 파일

사용법:
    python main.py --mock            # 샘플 CSV로 테스트, 이메일은 미리보기만
    python main.py --mock --send     # 샘플 CSV로 테스트, 실제 이메일 발송
    python main.py                   # 실제 구글 시트 연동 (서비스 계정 키 준비 후)
    python main.py --send            # 실제 구글 시트 연동 + 실제 이메일 발송
"""

import argparse
from datetime import date

from sheet_reader import get_items
from deadline_checker import filter_alerts
from emailer import send_alert


def run(mock: bool, send: bool, today: date | None = None) -> int:
    items = get_items(mock=mock)
    print(f"[조회 완료] 총 {len(items)}개 항목")

    alerts = filter_alerts(items, today=today)
    print(f"[대상 확인] 알림 대상 {len(alerts)}건")

    for item, d_day in alerts:
        send_alert(item, d_day, send=send)

    return len(alerts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="정산 마감 알리미")
    parser.add_argument("--mock", action="store_true", help="샘플 CSV로 테스트")
    parser.add_argument("--send", action="store_true", help="실제 이메일 발송 (기본값: 미리보기만)")
    args = parser.parse_args()

    run(mock=args.mock, send=args.send)
