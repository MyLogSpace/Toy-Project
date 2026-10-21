"""
데이터 검증 모듈

원본 데이터에서 필수 항목 누락, 형식 오류를 걸러내고
정상 데이터와 오류 데이터를 분리해서 반환합니다.
(공고의 "원본 데이터 오류 검증" 요구사항 대응)
"""

REQUIRED_FIELDS = ["담당자", "업무유형", "업무내용"]


def validate_rows(rows):
    valid_rows = []
    error_rows = []

    for idx, row in enumerate(rows, start=1):
        errors = _check_row(row)
        if errors:
            error_rows.append({"row_index": idx, "data": row, "errors": errors})
        else:
            valid_rows.append(row)

    return valid_rows, error_rows


def _check_row(row):
    errors = []
    for field in REQUIRED_FIELDS:
        value = (row.get(field) or "").strip()
        if not value:
            errors.append(f"'{field}' 항목 누락")

    count = (row.get("처리건수") or "").strip()
    if count and not count.isdigit():
        errors.append(f"'처리건수' 값이 숫자가 아님: {count}")

    return errors
