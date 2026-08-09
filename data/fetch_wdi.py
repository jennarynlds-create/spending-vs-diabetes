#!/usr/bin/env python3
"""Download selected WDI indicator CSVs from the datasets/world-development-indicators GitHub mirror.
Saves files to data/<friendly_name>.csv
"""
import os
from pathlib import Path
import requests

BASE = "https://raw.githubusercontent.com/datasets/world-development-indicators/main/indicators"

FILES = {
    "sh.sta.diab.zs": "data/diabetes_prevalence.csv",
    "ms.mil.xpnd.gd.zs": "data/military_expenditure_pct_gdp.csv",
    "sh.med.beds.zs": "data/hospital_beds_per_1000.csv",
    "ny.gdp.pcap.cd": "data/gdp_per_capita.csv",
    "sp.dyn.le00.in": "data/life_expectancy.csv",
    "sh.dth.ncom.zs": "data/ncd_deaths_pct.csv",
}

os.makedirs("data", exist_ok=True)

for code, out in FILES.items():
    url = f"{BASE}/{code}/data.csv"
    print(f"Downloading {code} -> {out} from {url}")
    r = requests.get(url)
    r.raise_for_status()
    Path(out).write_text(r.text, encoding="utf-8")

print("Done")
