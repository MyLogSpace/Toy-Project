# 정산 마감 알리미 (Deadline Alert Bot)

구글 스프레드시트에 정산/신고 항목과 마감일을 기록해두면, 마감일이 D-3 또는 D-1일 때
자동으로 이메일 알림을 보내는 Python 자동화 도구.

## 배경

인사·회계 실무에서 매월 반복되는 정산·신고 업무의 마감일을 수기로 관리하며 놓치기 쉬웠던
문제를, 구글 시트 기반의 자동 알림 시스템으로 해결하기 위해 만들었다.

## 구조

```
sheet_reader.py      구글 시트(또는 로컬 CSV)에서 항목 읽기
deadline_checker.py  오늘 날짜 기준 D-3/D-1 여부 판별
emailer.py           SMTP로 알림 이메일 발송 (미리보기 모드 지원)
main.py              전체 파이프라인 실행
scheduler.py         매일 정해진 시각에 자동 실행
config.py            환경변수 기반 설정 관리
```

## 빠른 시작 (API 키 없이 테스트)

```bash
pip install -r requirements.txt
python main.py --mock
```

`data/sample_deadlines.csv`의 샘플 데이터를 읽어, 오늘 날짜 기준 D-3/D-1 항목을
콘솔에 미리보기로 출력한다. 실제 이메일은 발송되지 않는다.

## 실제 구글 시트 + 이메일 연동

1. `.env.example`을 복사해 `.env` 생성 후 값 입력
2. Google Cloud Console에서 서비스 계정 생성 → JSON 키 다운로드 → 프로젝트 루트에 저장
3. 구글 시트를 서비스 계정 이메일과 공유(편집 권한)
4. 구글 계정에서 앱 비밀번호 발급 후 `.env`의 `SMTP_APP_PASSWORD`에 입력
5. 실행:

```bash
pip install -r requirements.txt
python main.py --send              # 1회 실행 + 실제 발송
python scheduler.py                # 매일 09:00 자동 실행 (계속 실행 상태 유지)
```

## 시트 컬럼 형식

| 항목명 | 담당자 | 마감일 | 알림상태 |
|---|---|---|---|
| 8월 급여정산 | 서하나 | 2026-08-29 | |

마감일은 `YYYY-MM-DD` 형식.

## 향후 확장 가능 방향

- Google Calendar API 연동으로 캘린더 이벤트 자동 생성
- 알림상태 컬럼에 발송 여부를 기록해 중복 발송 방지
- 슬랙 웹훅 연동
