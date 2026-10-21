"""
실행 로그 & 재시도 유틸리티

- setup_logger(): 실행 로그를 logs/execution.log 파일과 콘솔에 동시 기록
- with_retry(): 실패 시 지정된 횟수만큼 재시도하는 데코레이터
"""

import functools
import logging
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import config


def setup_logger():
    os.makedirs(config.LOG_DIR, exist_ok=True)
    log_path = os.path.join(config.LOG_DIR, "execution.log")

    logger = logging.getLogger("report_agent")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()


def with_retry(max_retries=None, backoff_seconds=None):
    """
    함수 실행 실패 시 자동 재시도.
    최종 실패하면 예외를 그대로 올려서 상위(main.py)에서 실패 알림을 보낼 수 있게 함.
    """
    max_retries = max_retries or config.MAX_RETRIES
    backoff_seconds = backoff_seconds or config.RETRY_BACKOFF_SECONDS

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    logger.warning(
                        f"'{func.__name__}' 실행 실패 (시도 {attempt}/{max_retries}): {e}"
                    )
                    if attempt < max_retries:
                        time.sleep(backoff_seconds)
            logger.error(f"'{func.__name__}' 최종 실패 - {max_retries}회 재시도 모두 실패")
            raise last_error

        return wrapper

    return decorator
