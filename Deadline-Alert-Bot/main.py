"""
정산 마감 알리미 - 메인 실행 파일

사용법:
    python main.py --mock                          # 샘플 CSV로 테스트, 이메일은 미리보기만
    python main.py --mock --today 2026-08-26       # 기준일을 지정해서 테스트 (샘플 데이터는 2026년 8~9월 마감)
    python main.py --mock --send                   # 샘플 CSV로 테스트, 실제 이메일 발송
    python main.py                                 # 실제 구글 시트 연동 (서비스 계정 키 준비 후)
    python main.py --send                          # 실제 구글 시트 연동 + 실제 이메일 발송
"""

import argparse
from datetime import date, datetime

from sheet_reader import get_items
from deadline_checker import filter_alerts
from emailer import send_alert


def run(mock: bool, send: bool, today: date | None = None) -> int:
    items = get_items(mock=mock)
    print(f"[조회 완료] 총 {len(items)}개 항목")

    base = today or date.today()
    print(f"[기준 날짜] {base.isoformat()}")

    alerts = filter_alerts(items, today=base)
    print(f"[대상 확인] 알림 대상 {len(alerts)}건")

    for item, d_day in alerts:
        send_alert(item, d_day, send=send)

    return len(alerts)


def _parse_today(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError("날짜는 YYYY-MM-DD 형식으로 입력하세요. 예: 2026-08-26")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="정산 마감 알리미")
    parser.add_argument("--mock", action="store_true", help="샘플 CSV로 테스트")
    parser.add_argument("--send", action="store_true", help="실제 이메일 발송 (기본값: 미리보기만)")
    parser.add_argument("--today", type=_parse_today, default=None,
                        help="기준 날짜 지정 (YYYY-MM-DD). 생략하면 오늘 날짜")
    args = parser.parse_args()

    run(mock=args.mock, send=args.send, today=args.today)
