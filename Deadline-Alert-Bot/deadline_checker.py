"""
오늘 날짜를 기준으로, 마감일이 알림 대상(D-3, D-1 등)인 항목을 골라낸다.
"""

from datetime import date

import config
from sheet_reader import DeadlineItem


def days_until(due: date, today: date) -> int:
    return (due - today).days


def filter_alerts(items: list[DeadlineItem], today: date | None = None) -> list[tuple[DeadlineItem, int]]:
    """
    알림 대상 항목과 D-day 값을 튜플로 반환한다.
    예: [(item, 3), (item2, 1)]
    """
    today = today or date.today()
    alerts = []
    for item in items:
        d = days_until(item.due_date, today)
        if d in config.ALERT_DAYS_BEFORE:
            alerts.append((item, d))
    return alerts
