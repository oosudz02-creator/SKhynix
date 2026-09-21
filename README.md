# SK hynix DART Financial Analysis

SK하이닉스의 DART XBRL 재무자료를 기반으로 주요 재무데이터를 추출하고 재무비율을 계산한 프로젝트입니다.

## Source
- DART XBRL: `data/entity00164779_2025-12-31.xbrl`
- 분석 기준: 연결재무제표, KRW
- 대상 기간: FY2023–FY2025
- 재무비율 정의: 첨부된 `재무제표_재무비율_실무가이드.docx`의 정의를 기본으로 적용

## Repository structure
```text
SKhynix/
├── README.md
├── requirements.txt
├── data/
│   ├── entity00164779_2025-12-31.xbrl
│   ├── financial_data.csv
│   └── financial_ratios.csv
├── report/
│   └── financial_ratio_analysis.md
└── src/
    └── analyze_financials.py
```

## Main analysis
- 성장성: 매출증가율
- 수익성: 매출총이익률, 영업이익률, 순이익률, ROA, ROE
- 유동성/재무안정성: 유동비율, 부채비율, 자기자본비율
- 현금흐름: CFO/순이익, FCF
- 차입부담: 순차입금, EBITDA, 순차입금/EBITDA, 영업이익/금융비용

## Reproduce
```bash
python src/analyze_financials.py
```

> 주의: FCF와 EBITDA는 정의에 따라 조정 범위가 달라질 수 있습니다. 이 프로젝트에서는 FCF = CFO - CAPEX, EBITDA = 영업이익 + 현금흐름표의 감가상각·무형자산상각 조정액으로 계산했습니다.
