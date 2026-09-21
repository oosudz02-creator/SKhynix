"""Fetch SK hynix financial statements from OpenDART.

Example:
    python scripts/fetch_dart_financials.py --year 2025 --report annual --fs CFS
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.dart.client import DartClient  # noqa: E402


REPORT_CODES = {
    "q1": "11013",
    "half": "11012",
    "q3": "11014",
    "annual": "11011",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2025)
    parser.add_argument(
        "--report",
        choices=REPORT_CODES,
        default="annual",
        help="q1, half, q3, annual",
    )
    parser.add_argument(
        "--fs",
        choices=["CFS", "OFS"],
        default="CFS",
        help="CFS=연결, OFS=별도",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    config_path = ROOT / "config" / "company.json"
    company = json.loads(config_path.read_text(encoding="utf-8"))

    corp_code = company["corp_code"]
    report_code = REPORT_CODES[args.report]

    client = DartClient()

    print(f"[1/3] 기업정보 조회: {company['company_name']}")
    company_info = client.get_company(corp_code)

    print(
        f"      DART: {company_info.get('corp_name')} / "
        f"종목코드: {company_info.get('stock_code')}"
    )

    print(
        f"[2/3] 재무제표 조회: {args.year} / "
        f"{args.report}({report_code}) / {args.fs}"
    )
    data = client.get_full_financial_statement(
        corp_code=corp_code,
        bsns_year=args.year,
        reprt_code=report_code,
        fs_div=args.fs,
    )

    raw_dir = ROOT / "data" / "raw" / "dart"
    processed_dir = ROOT / "data" / "processed"
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    raw_path = raw_dir / f"{args.year}_{report_code}_{args.fs}.json"
    raw_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    rows = data.get("list", [])
    df = pd.DataFrame(rows)

    # 금액 열은 분석 단계에서 숫자로 변환하기 쉽게 정리한다.
    amount_cols = [
        "thstrm_amount",
        "thstrm_add_amount",
        "frmtrm_amount",
        "frmtrm_add_amount",
        "bfefrmtrm_amount",
    ]
    for col in amount_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype("string")
                .str.replace(",", "", regex=False)
                .replace("", pd.NA)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    csv_path = (
        processed_dir
        / f"financials_{args.year}_{args.report}_{args.fs}.csv"
    )
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    print(f"[3/3] 완료")
    print(f"      Raw JSON : {raw_path}")
    print(f"      CSV      : {csv_path}")
    print(f"      Rows     : {len(df):,}")

    if df.empty:
        print("주의: 조회된 재무제표 행이 없습니다.")
    else:
        print("\n주요 계정 샘플:")
        sample_cols = [
            c for c in
            ["sj_div", "account_nm", "thstrm_amount", "frmtrm_amount"]
            if c in df.columns
        ]
        print(df[sample_cols].head(15).to_string(index=False))


if __name__ == "__main__":
    main()
