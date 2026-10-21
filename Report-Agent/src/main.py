"""
사내 보고서 생성 에이전트 - 메인 실행 파일

실행: python src/main.py

전체 흐름:
  1. Google Sheets(목업: CSV) 원본 데이터 로드
  2. 데이터 검증 (누락/오류 항목 분리)
  3. AI 보고서 초안 생성 (재시도 로직 적용)
  4. Slack(목업: 터미널 + HTML 카드) 승인 요청 - 반려 시 재작성 루프
  5. 최종 발송 및 저장 + 실행 로그 기록
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import config
from logger_utils import logger, with_retry
from data_loader import load_source_data
from validator import validate_rows
from report_generator import generate_report
from approval import request_approval
from notifier import send_final_report, notify_failure

MAX_REGENERATIONS = 2


@with_retry()
def _generate_with_retry(valid_rows, error_rows):
    # SIMULATE_FAILURE=1 환경변수를 걸면 재시도 로직이 실제로 동작하는 걸 데모로 보여줄 수 있음
    if os.environ.get("SIMULATE_FAILURE") == "1":
        raise ConnectionError("LLM API 응답 지연 (데모용 강제 실패)")
    return generate_report(valid_rows, error_rows)


def run_pipeline():
    logger.info("=== 사내 보고서 생성 에이전트 실행 시작 ===")
    logger.info(f"실행 모드: {'MOCK' if config.MOCK_MODE else 'LIVE'}")

    # 1. 데이터 수집
    rows = load_source_data()
    logger.info(f"원본 데이터 {len(rows)}건 로드 완료")

    # 2. 데이터 검증
    valid_rows, error_rows = validate_rows(rows)
    logger.info(f"검증 완료 - 정상 {len(valid_rows)}건 / 오류 {len(error_rows)}건")
    if error_rows:
        for err in error_rows:
            logger.warning(f"검증 오류 {err['row_index']}행: {err['errors']}")

    # 3. AI 보고서 초안 생성 (실패 시 자동 재시도)
    try:
        report_text = _generate_with_retry(valid_rows, error_rows)
    except Exception as e:
        notify_failure(f"보고서 생성 최종 실패: {e}")
        return

    # 4. 승인 요청 (반려 시 최대 MAX_REGENERATIONS회 재작성)
    attempt = 0
    approved = request_approval(report_text)
    while not approved and attempt < MAX_REGENERATIONS:
        attempt += 1
        logger.info(f"반려됨 - 보고서 재작성 시도 {attempt}/{MAX_REGENERATIONS}")
        report_text = _generate_with_retry(valid_rows, error_rows)
        approved = request_approval(report_text)

    if not approved:
        notify_failure("승인 재시도 초과 - 담당자 직접 확인 필요")
        return

    # 5. 최종 발송 및 저장
    output_path = send_final_report(report_text)
    logger.info(f"=== 실행 완료 - 최종 보고서: {output_path} ===")


if __name__ == "__main__":
    run_pipeline()
