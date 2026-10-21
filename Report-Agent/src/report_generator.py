"""
AI 보고서 초안 생성 모듈

목업 모드: 실제 LLM 호출 없이, 데이터를 요약한 템플릿 기반 보고서를 생성
실제 모드: OpenAI API(+ LangChain)로 자연어 보고서 초안을 생성

두 모드 모두 반환 형식은 동일한 문자열이라, main.py 쪽 코드는
MOCK_MODE 값과 무관하게 동일하게 동작합니다.
"""

import sys
import os
from collections import Counter
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import config


def generate_report(valid_rows, error_rows):
    if config.MOCK_MODE:
        return _generate_mock_report(valid_rows, error_rows)
    else:
        return _generate_llm_report(valid_rows, error_rows)


def _generate_mock_report(valid_rows, error_rows):
    """실제 API 없이도 데모가 가능한 템플릿 기반 보고서 생성"""
    today = datetime.now().strftime("%Y-%m-%d")
    type_counter = Counter(row.get("업무유형", "") for row in valid_rows)
    status_counter = Counter(row.get("처리상태", "") for row in valid_rows)

    lines = []
    lines.append(f"[경영지원팀 주간 업무 보고서 - {today}]")
    lines.append("")
    lines.append(f"이번 주 총 처리 업무: {len(valid_rows)}건 (검증 제외 {len(error_rows)}건)")
    lines.append("")
    lines.append("- 업무유형별 현황")
    for biz_type, cnt in type_counter.items():
        label = biz_type if biz_type else "(미분류)"
        lines.append(f"  · {label}: {cnt}건")
    lines.append("")
    lines.append("- 처리상태별 현황")
    for status, cnt in status_counter.items():
        label = status if status else "(미기재)"
        lines.append(f"  · {label}: {cnt}건")

    if error_rows:
        lines.append("")
        lines.append("- 데이터 검증 이슈 (담당자 확인 필요)")
        for err in error_rows:
            lines.append(f"  · {err['row_index']}행: {', '.join(err['errors'])}")

    return "\n".join(lines)


def _generate_llm_report(valid_rows, error_rows):
    """
    실제 연동부 (MOCK_MODE = False 일 때 사용)

    pip install openai langchain-openai 필요

    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate

    llm = ChatOpenAI(model=config.LLM_MODEL, api_key=config.OPENAI_API_KEY)
    prompt = ChatPromptTemplate.from_template(
        "다음 업무 데이터를 바탕으로 경영지원팀 주간 업무 보고서를 "
        "간결한 항목 형식으로 작성해줘.\\n\\n데이터: {data}\\n오류 항목: {errors}"
    )
    chain = prompt | llm
    result = chain.invoke({"data": valid_rows, "errors": error_rows})
    return result.content
    """
    raise NotImplementedError(
        "실제 LLM 연동은 MOCK_MODE=False 설정 후 "
        "OPENAI_API_KEY 발급 및 위 주석 코드를 활성화하세요."
    )
