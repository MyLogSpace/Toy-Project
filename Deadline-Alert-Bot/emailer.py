"""
마감 임박 알림 이메일을 발송하는 모듈.
- send=False로 두면 실제 발송 없이 내용만 콘솔에 출력한다 (테스트/미리보기용).
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config
from sheet_reader import DeadlineItem


def build_subject(item: DeadlineItem, d_day: int) -> str:
    return f"[마감 D-{d_day}] {item.name} 마감이 {d_day}일 남았습니다"


def build_body(item: DeadlineItem, d_day: int) -> str:
    return (
        f"안녕하세요.\n\n"
        f"'{item.name}' 항목의 마감일이 {d_day}일 남았습니다.\n\n"
        f"- 담당자: {item.owner}\n"
        f"- 마감일: {item.due_date.isoformat()}\n\n"
        f"기한 내 처리를 부탁드립니다."
    )


def send_alert(item: DeadlineItem, d_day: int, send: bool = False) -> None:
    subject = build_subject(item, d_day)
    body = build_body(item, d_day)

    if not send:
        print("=" * 50)
        print("[미리보기 모드 - 실제 발송 안 됨]")
        print(f"To      : {config.ALERT_RECEIVER}")
        print(f"Subject : {subject}")
        print(f"Body    :\n{body}")
        print("=" * 50)
        return

    msg = MIMEMultipart()
    msg["From"] = config.SMTP_USERNAME
    msg["To"] = config.ALERT_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT) as server:
        server.login(config.SMTP_USERNAME, config.SMTP_APP_PASSWORD)
        server.send_message(msg)
    print(f"[발송 완료] {config.ALERT_RECEIVER} <- {subject}")
