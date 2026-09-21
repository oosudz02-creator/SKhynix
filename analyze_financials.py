from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data" / "financial_data.csv"
OUT = Path(__file__).resolve().parents[1] / "data" / "financial_ratios_recalculated.csv"

df = pd.read_csv(DATA)
df["revenue_growth"] = df["revenue"].pct_change()
df["gross_margin"] = df["gross_profit"] / df["revenue"]
df["operating_margin"] = df["operating_income"] / df["revenue"]
df["net_margin"] = df["net_income"] / df["revenue"]
df["current_ratio"] = df["current_assets"] / df["current_liabilities"]
df["debt_to_equity"] = df["liabilities"] / df["equity"]
df["equity_ratio"] = df["equity"] / df["assets"]
df["cfo_to_net_income"] = df["cfo"] / df["net_income"]
df["capex_total"] = df["capex_ppe"] + df["capex_intangible"]
df["fcf"] = df["cfo"] - df["capex_total"]
df["net_debt"] = df["borrowings"] - df["cash_and_equivalents"]
df["ebitda"] = df["operating_income"] + df["depreciation_for_ebitda"] + df["amortisation_for_ebitda"]
df["net_debt_to_ebitda"] = df["net_debt"] / df["ebitda"]
df["operating_income_to_finance_costs"] = df["operating_income"] / df["finance_costs"]
df["roa"] = df["net_income"] / ((df["assets"] + df["assets"].shift(1)) / 2)
df["roe"] = df["net_income"] / ((df["equity"] + df["equity"].shift(1)) / 2)
df.to_csv(OUT, index=False)
print(df.round(4).to_string(index=False))
