"""
매일 정해진 시각에 main.run()을 자동 실행한다.
로컬/서버에서 계속 켜둘 프로세스로 사용 (또는 cron에 main.py 직접 등록해도 무방).

사용법:
    python scheduler.py
"""

import time
import schedule

from main import run

RUN_TIME = "09:00"  # 매일 오전 9시


def job():
    print(f"[실행] {time.strftime('%Y-%m-%d %H:%M:%S')}")
    run(mock=False, send=True)


if __name__ == "__main__":
    schedule.every().day.at(RUN_TIME).do(job)
    print(f"스케줄러 시작. 매일 {RUN_TIME}에 실행됩니다. (Ctrl+C로 종료)")
    while True:
        schedule.run_pending()
        time.sleep(60)
