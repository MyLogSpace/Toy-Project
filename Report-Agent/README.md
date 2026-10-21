[README.md](https://github.com/user-attachments/files/33766439/README.md)
# 사내 보고서 생성 에이전트 (Report Agent)

Google Sheets(또는 CSV) 원본 데이터를 읽어 AI가 보고서 초안을 작성하고,
담당자 승인(Human-in-the-loop)을 거쳐 최종 발송까지 자동화하는 에이전트입니다.

**[▶ 데모 보기](https://mylogspace.github.io/Toy-Project/Report-Agent/Demo/)** — 실행 로그와 승인/반려 흐름을 눌러볼 수 있는 시뮬레이션 페이지

> 데모 페이지는 `python src/main.py`의 로그 흐름과 승인 카드를 브라우저에서 재현한 것입니다.

## Problem

경영지원 업무를 하며 주간/월간 보고서를 만들 때마다 여러 시트에 흩어진 데이터를
직접 취합하고, 오류를 손으로 걸러낸 뒤, 같은 형식으로 정리해서 보고하는 과정을
매번 반복해야 했습니다. 반복되지만 사람이 최종 확인은 반드시 해야 하는 업무였습니다.

## Decision

- 데이터 취합 → 검증 → AI 초안 생성 → 사람 승인 → 발송 순서로 파이프라인을 설계
- 승인 없이 바로 발송하지 않고, 반드시 담당자 확인을 거치는 **Human-in-the-loop** 구조를 넣음
- 실행 중 실패해도 자동으로 재시도하고, 최종 실패 시에는 관리자에게 알림이 가도록 설계
- 포트폴리오 데모 목적이므로, 외부 API 없이도 전체 흐름을 확인할 수 있게 **MOCK_MODE**를 기본값으로 둠

## Result

- CLI로 전체 파이프라인이 목업 모드에서 end-to-end로 동작 (데이터 로드 → 검증 → 초안 생성 → 승인 → 발송)
- 검증 단계에서 결측 데이터를 걸러내고, 강제 실패 시뮬레이션(`SIMULATE_FAILURE`)으로 재시도 로직이 동작함을 확인
- 승인 단계는 Slack 카드를 모사한 HTML 미리보기(`approval_ui/preview_card.html`)로 시각화

## 현재 구현 범위

| 구분 | 상태 |
|---|---|
| 목업 모드 (CSV → 검증 → 템플릿 보고서 → 터미널 승인 → 파일 저장) | 구현 및 동작 확인 |
| Google Sheets / OpenAI / Slack / SMTP 실연동 | 구조와 코드 예시만 작성 (미구현, `NotImplementedError`) |

실연동은 각 모듈의 "실제 연동부" 주석에 예시 코드가 있지만, 단순히 주석을 해제하는 것만으로는 완성되지 않습니다.
특히 Slack 승인은 버튼 클릭 결과를 받을 별도 엔드포인트 서버가 필요합니다.

## 직무 역량 대응표

| 요구 역량 | 구현 위치 |
|---|---|
| Excel·CSV·Google Sheets 기반 반복업무 | `src/data_loader.py` |
| 원본 데이터 취합 및 검증 | `src/validator.py` |
| 사내 보고·문서 생성 | `src/report_generator.py` |
| Human-in-the-loop 승인 구조 | `src/approval.py` |
| 실행 로그·오류 알림·재시도·재처리 | `src/logger_utils.py`, `src/main.py` |
| 외부 서비스 API 연동 (확장 가능 구조) | 각 모듈 내 "실제 연동부" 주석 |

## 실행 방법

표준 라이브러리만 사용하므로 목업 모드는 별도 설치가 필요 없습니다. (Python 3.8 이상)

```bash
python src/main.py
```

- 실행하면 콘솔에 보고서 초안이 출력되고, `y`/`n`으로 승인/반려를 입력받습니다.
- 승인하면 `outputs/` 폴더에 최종 보고서가 저장됩니다.
- 실행 로그는 `logs/execution.log`에서 확인할 수 있습니다.
- 승인 카드 미리보기는 `approval_ui/preview_card.html`을 브라우저로 열어 확인하세요.

재시도 로직 데모(강제 실패 시뮬레이션):

```bash
# macOS / Linux
SIMULATE_FAILURE=1 python src/main.py

# Windows PowerShell
$env:SIMULATE_FAILURE=1; python src/main.py

# Windows CMD
set SIMULATE_FAILURE=1 && python src/main.py
```

## 실제 API로 전환하려면

`config.py`에서 `MOCK_MODE = False`로 바꾸고, 아래 모듈의 "실제 연동부"를 구현해야 합니다.
API 키는 코드에 적지 말고 환경변수(`GOOGLE_SHEET_ID`, `OPENAI_API_KEY`, `SLACK_WEBHOOK_URL`, `NOTIFY_EMAIL`)로 설정합니다.

1. `src/data_loader.py` → Google Sheets API (gspread)
2. `src/report_generator.py` → OpenAI API + LangChain
3. `src/approval.py`, `src/notifier.py` → Slack Webhook(+Interactivity 서버) / SMTP 이메일

필요한 패키지는 `requirements.txt`에 정리되어 있습니다.

## 폴더 구조

```
Report-Agent/
├── config.py              # MOCK_MODE 등 전역 설정
├── requirements.txt
├── data/
│   └── sample_report_data.csv   # 데모용 샘플 원본 데이터
├── src/
│   ├── data_loader.py     # 원본 데이터 수집
│   ├── validator.py       # 데이터 검증
│   ├── report_generator.py# AI 보고서 초안 생성
│   ├── approval.py        # Human-in-the-loop 승인
│   ├── notifier.py        # 최종 발송/저장
│   ├── logger_utils.py    # 실행 로그 + 재시도
│   └── main.py            # 전체 파이프라인 실행
├── approval_ui/
│   └── preview_card.html  # 승인 카드 미리보기 (실행 시 갱신됨)
├── Demo/
│   └── index.html         # GitHub Pages 데모 페이지
├── outputs/                # 최종 보고서 저장 위치 (실행 시 생성)
└── logs/
    └── execution.log       # 실행 로그 (실행 시 생성)
```
