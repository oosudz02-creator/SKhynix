# SKhynix DART Financial Agent

SK하이닉스의 OpenDART 재무데이터를 수집하고, 이후 재무비율/분석 Agent로 확장하기 위한 기본 저장소입니다.

## 1. 구조

```text
SKhynix/
├─ .github/workflows/
│  └─ dart_update.yml
├─ config/
│  └─ company.json
├─ data/
│  ├─ raw/dart/
│  └─ processed/
├─ src/dart/
│  ├─ __init__.py
│  └─ client.py
├─ scripts/
│  └─ fetch_dart_financials.py
├─ .env.example
├─ .gitignore
└─ requirements.txt
```

## 2. DART API Key

`.env.example`을 `.env`로 복사한 뒤 API 키를 입력합니다.

```text
DART_API_KEY=발급받은_40자리_키
```

`.env`는 `.gitignore`에 포함되어 GitHub에 올라가지 않습니다.

## 3. 실행

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Copy-Item .env.example .env
# .env에 DART_API_KEY 입력

python scripts/fetch_dart_financials.py --year 2025 --report annual --fs CFS
```

실행하면 다음이 생성됩니다.

```text
data/raw/dart/2025_11011_CFS.json
data/processed/financials_2025_annual_CFS.csv
```

## 4. SK하이닉스 식별정보

- 회사명: 에스케이하이닉스(주)
- 종목코드: 000660
- DART corp_code: 00164779

## 5. 다음 개발 단계

1. 10년 연간/분기 데이터 수집
2. 계정명 표준화(account mapping)
3. 재무비율 계산
4. 데이터 검증
5. AI 분석 Agent
6. GitHub Actions 자동 업데이트
7. Dashboard
