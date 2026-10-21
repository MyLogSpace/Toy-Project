"""
승인 요청 모듈 (Human-in-the-loop)

목업 모드: 실제 Slack 앱 없이도 데모 가능하도록
  1) 보고서 초안을 Slack 카드 형태의 HTML(preview_card.html)로 생성
  2) 터미널에서 y/n 입력을 받아 "승인 버튼 클릭"을 시뮬레이션

실제 모드: Slack Incoming Webhook + Interactivity로 대체 (하단 주석 참고)
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import config
from logger_utils import logger

APPROVAL_UI_DIR = os.path.join(config.BASE_DIR, "approval_ui")

CARD_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head><meta charset="UTF-8"><title>보고서 승인 요청 (미리보기)</title>
<style>
  body {{ font-family: sans-serif; background:#f4f7f9; padding:32px; }}
  .card {{ max-width:480px; margin:0 auto; background:#fff; border-radius:8px;
           border:1px solid #E1E4E8; padding:24px; box-shadow:0 1px 3px rgba(0,0,0,0.08); }}
  .card h2 {{ font-size:16px; color:#3E617A; margin:0 0 12px; }}
  .card pre {{ white-space:pre-wrap; font-size:13px; color:#333; line-height:1.6; }}
  .btns {{ margin-top:16px; }}
  .btn {{ padding:8px 16px; border-radius:6px; border:none; font-size:13px; margin-right:8px; }}
  .approve {{ background:#3E617A; color:#fff; }}
  .reject {{ background:#eee; color:#555; }}
</style></head>
<body>
  <div class="card">
    <h2>사내 보고서 생성 에이전트 - 승인 요청</h2>
    <pre>{report_text}</pre>
    <div class="btns">
      <button class="btn approve">승인</button>
      <button class="btn reject">반려</button>
    </div>
  </div>
</body>
</html>
"""


def request_approval(report_text):
    if config.MOCK_MODE:
        return _mock_approval_flow(report_text)
    else:
        return _slack_approval_flow(report_text)


def _mock_approval_flow(report_text):
    os.makedirs(APPROVAL_UI_DIR, exist_ok=True)
    preview_path = os.path.join(APPROVAL_UI_DIR, "preview_card.html")
    with open(preview_path, "w", encoding="utf-8") as f:
        f.write(CARD_TEMPLATE.format(report_text=report_text))

    logger.info(f"승인 요청 카드 생성됨: {preview_path}")
    print("\n" + "=" * 50)
    print("[Slack 승인 요청 미리보기]")
    print(report_text)
    print("=" * 50)

    answer = input("\n이 보고서를 승인하시겠습니까? (y=승인 / n=반려): ").strip().lower()
    approved = answer == "y"
    logger.info(f"승인 결과: {'승인' if approved else '반려'}")
    return approved


def _slack_approval_flow(report_text):
    """
    실제 연동부 (MOCK_MODE = False 일 때 사용)

    Slack Incoming Webhook으로 카드 메시지를 보내고,
    버튼 클릭은 Slack Interactivity(별도 엔드포인트 서버)로 콜백을 받아 처리합니다.

    import requests
    payload = {
        "text": "보고서 승인 요청",
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": report_text}},
            {"type": "actions", "elements": [
                {"type": "button", "text": {"type": "plain_text", "text": "승인"}, "value": "approve"},
                {"type": "button", "text": {"type": "plain_text", "text": "반려"}, "value": "reject"},
            ]},
        ],
    }
    requests.post(config.SLACK_WEBHOOK_URL, json=payload)
    # 실제로는 버튼 클릭 결과를 별도 웹훅 서버에서 받아 승인 여부를 반환해야 함
    """
    raise NotImplementedError(
        "실제 Slack 연동은 MOCK_MODE=False 설정 후 "
        "SLACK_WEBHOOK_URL 발급 및 Interactivity 엔드포인트 구축이 필요합니다."
    )
