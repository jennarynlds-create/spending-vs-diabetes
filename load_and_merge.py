"""
load_and_merge.py

Loads real World Bank World Development Indicators data (via the
datasets/world-development-indicators GitHub mirror) and merges six
indicators into a single country-year panel for analysis:

  - Diabetes prevalence, % of adults 20-79   (sh.sta.diab.zs)
  - Military expenditure, % of GDP           (ms.mil.xpnd.gd.zs)
  - Hospital beds per 1,000 people           (sh.med.beds.zs)
  - GDP per capita, current US$              (ny.gdp.pcap.cd)
  - Life expectancy at birth, years          (sp.dyn.le00.in)
  - Deaths from non-communicable disease, %  (sh.dth.ncom.zs)

Source data license: CC BY-4.0 (World Bank).

Run: python load_and_merge.py
Output: merged_panel.csv
"""

import pandas as pd

FILES = {
    "diabetes_prevalence_pct": "data/diabetes_prevalence.csv",
    "military_exp_pct_gdp": "data/military_expenditure_pct_gdp.csv",
    "hospital_beds_per_1000": "data/hospital_beds_per_1000.csv",
    "gdp_per_capita_usd": "data/gdp_per_capita.csv",
    "life_expectancy_years": "data/life_expectancy.csv",
    "ncd_deaths_pct": "data/ncd_deaths_pct.csv",
}

# World Bank aggregate rows (regions, income groups) to exclude so the
# analysis reflects individual countries only.
NON_COUNTRY_CODES = {
    "AFE", "AFW", "ARB", "CEB", "CSS", "EAP", "EAR", "EAS", "ECA", "ECS",
    "EMU", "EUU", "FCS", "HIC", "HPC", "IBD", "IBT", "IDA", "IDB", "IDX",
    "LAC", "LCN", "LDC", "LIC", "LMC", "LMY", "LTE", "MEA", "MIC", "MNA",
    "NAC", "OED", "OSS", "PRE", "PSS", "PST", "SAS", "SSA", "SSF", "SST",
    "TEA", "TEC", "TLA", "TMN", "TSA", "TSS", "UMC", "WLD", "INX",
}

frames = []
for col_name, path in FILES.items():
    df = pd.read_csv(path)
    df = df[~df["Country Code"].isin(NON_COUNTRY_CODES)]
    df = df.rename(columns={"Country Name": "country", "Country Code": "code",
                             "Year": "year", "Value": col_name})
    df = df[["country", "code", "year", col_name]]
    frames.append(df)

# Merge all indicators on country/year. Most WDI indicators aren't reported
# every year, so we keep the most recent available value per country for
# each indicator (as of its own latest data point) rather than forcing a
# single shared year, which would drop most countries.
latest = []
for df in frames:
    idx = df.groupby("code")["year"].idxmax()
    latest.append(df.loc[idx].drop(columns="year"))

merged = latest[0]
for df in latest[1:]:
    merged = merged.merge(df.drop(columns="country"), on="code", how="outer")

merged = merged.dropna(subset=["diabetes_prevalence_pct"])  # anchor on diabetes data being present
merged = merged.sort_values("diabetes_prevalence_pct", ascending=False)
merged.to_csv("merged_panel.csv", index=False)

print(f"Merged panel: {len(merged)} countries with diabetes prevalence data")
print(merged.head(10)[["country", "diabetes_prevalence_pct", "military_exp_pct_gdp", "hospital_beds_per_1000"]])
