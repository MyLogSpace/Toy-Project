"""
최종 발송 & 저장 모듈

목업 모드: outputs/ 폴더에 최종 보고서를 파일로 저장 + 콘솔에 발송 로그 출력
실제 모드: 이메일(SMTP) 또는 Slack 채널로 실제 발송
"""

import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import config
from logger_utils import logger


def send_final_report(report_text):
    if config.MOCK_MODE:
        return _mock_send(report_text)
    else:
        return _real_send(report_text)


def _mock_send(report_text):
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    output_path = os.path.join(config.OUTPUT_DIR, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    logger.info(f"[발송 완료 - 목업] 최종 보고서 저장: {output_path}")
    logger.info(f"[발송 완료 - 목업] 수신자: {config.NOTIFY_EMAIL} (실제 발송 없음)")
    return output_path


def notify_failure(error_message):
    logger.error(f"[실패 알림] {error_message}")
    if config.MOCK_MODE:
        print(f"\n[관리자 알림 - 목업] 자동화 실패: {error_message}")


def _real_send(report_text):
    """
    실제 연동부 (MOCK_MODE = False 일 때 사용)

    import smtplib
    from email.mime.text import MIMEText

    msg = MIMEText(report_text)
    msg["Subject"] = "주간 업무 보고서"
    msg["To"] = config.NOTIFY_EMAIL

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("your_email@gmail.com", "app_password")
        server.send_message(msg)
    """
    raise NotImplementedError(
        "실제 이메일/Slack 발송은 MOCK_MODE=False 설정 후 "
        "SMTP 계정 또는 Slack 채널 설정이 필요합니다."
    )
