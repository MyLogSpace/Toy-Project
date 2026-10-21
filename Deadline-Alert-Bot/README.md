[README.md](https://github.com/user-attachments/files/33766399/README.md)
# 정산 마감 알리미 (Deadline Alert Bot)

구글 스프레드시트에 정산/신고 항목과 마감일을 기록해두면, 마감일이 D-3 또는 D-1일 때
자동으로 이메일 알림을 보내는 Python 자동화 도구.

**[▶ 데모 보기](https://mylogspace.github.io/Toy-Project/Deadline-Alert-Bot/Demo/)** — 기준 날짜를 바꿔가며 어떤 항목에 알림이 가는지 확인할 수 있는 시뮬레이션 페이지

> 데모 페이지는 `main.py --mock`의 출력과 이메일 본문을 브라우저에서 재현한 것이며, 실제 발송은 이루어지지 않습니다.

## 배경

인사·회계 실무에서 매월 반복되는 정산·신고 업무의 마감일을 수기로 관리하며 놓치기 쉬웠던
문제를, 구글 시트 기반의 자동 알림으로 해결해 보기 위해 만든 자동화 연습 프로젝트입니다.

## 구조

```
Deadline-Alert-Bot/
├── main.py              전체 파이프라인 실행
├── sheet_reader.py      구글 시트(또는 로컬 CSV)에서 항목 읽기
├── deadline_checker.py  기준 날짜 대비 D-3/D-1 여부 판별
├── emailer.py           SMTP로 알림 이메일 발송 (미리보기 모드 지원)
├── scheduler.py         매일 정해진 시각에 자동 실행
├── config.py            환경변수 기반 설정 관리
├── .env.example         환경변수 템플릿 (값은 비어 있음)
├── requirements.txt
├── data/
│   └── sample_deadlines.csv   데모용 샘플 데이터
└── Demo/
    └── index.html       GitHub Pages 데모 페이지
```

## 빠른 시작 (API 키 없이 테스트)

**Python 3.10 이상**이 필요합니다.

```bash
pip install -r requirements.txt
python main.py --mock --today 2026-08-26
```

샘플 데이터(`data/sample_deadlines.csv`)의 마감일이 2026년 8~9월이므로,
`--today`로 기준 날짜를 지정해야 알림 대상이 나옵니다. (생략하면 실행 당일 기준이라 대상이 없을 수 있습니다.)
실제 이메일은 발송되지 않고 내용만 콘솔에 출력됩니다.

예상 출력:

```
[조회 완료] 총 4개 항목
[기준 날짜] 2026-08-26
[대상 확인] 알림 대상 2건
(8월 급여정산 D-3, 부가세 신고 D-1 이메일 미리보기)
```

## 실제 구글 시트 + 이메일 연동

> 이 구간은 코드가 작성되어 있으나, 실제 계정으로 end-to-end 검증을 마친 것은 아닙니다. (mock 모드로 검증)

1. `.env.example`을 복사해 `.env` 생성 후 값 입력
2. Google Cloud Console에서 서비스 계정 생성 → JSON 키 다운로드 → 프로젝트 루트에 저장
3. 구글 시트를 서비스 계정 이메일과 공유(편집 권한)
4. 구글 계정에서 앱 비밀번호 발급 후 `.env`의 `SMTP_APP_PASSWORD`에 입력
5. 실행:

```bash
pip install -r requirements.txt
python main.py --send              # 1회 실행 + 실제 발송
python scheduler.py                # 매일 09:00 자동 실행 (프로세스를 계속 켜둬야 함)
```

> `.env`와 `service_account.json`은 `.gitignore`에 포함되어 있습니다. 절대 GitHub에 올리지 마세요.

## 시트 컬럼 형식

| 항목명 | 담당자 | 마감일 | 알림상태 |
|---|---|---|---|
| 8월 급여정산 | (담당자명) | 2026-08-29 | |

- 마감일은 `YYYY-MM-DD` 형식입니다.
- `알림상태` 컬럼은 현재 코드에서 사용하지 않습니다. (중복 발송 방지용으로 예약해 둔 컬럼)

## 한계와 향후 개선

- 같은 날 두 번 실행하면 알림이 중복 발송됩니다. → `알림상태` 컬럼에 발송 여부를 기록해 방지 예정
- `scheduler.py`는 프로세스를 계속 켜둬야 하므로, GitHub Actions 스케줄 등으로 대체 검토
- Google Calendar API 연동으로 캘린더 이벤트 자동 생성
- 슬랙 웹훅 연동
