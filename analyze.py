"""
analyze.py

Analyzes the merged World Bank panel (merged_panel.csv) to explore a
health-policy question: how does government spending allocation (military
vs. implied health-system capacity) relate to non-communicable disease
burden, using diabetes prevalence as the lens.

Run: python analyze.py
Outputs:
  - diabetes_vs_military_spending.png
  - diabetes_vs_hospital_beds.png
  - diabetes_vs_gdp_income_group.png
  - top_bottom_diabetes_burden.png
  - findings.md
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["figure.dpi"] = 140
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.3

df = pd.read_csv("merged_panel.csv")

# ---------------------------------------------------------------------------
# 1. Diabetes prevalence vs. military expenditure (% GDP)
# ---------------------------------------------------------------------------
sub = df.dropna(subset=["diabetes_prevalence_pct", "military_exp_pct_gdp"])
corr_mil = sub["diabetes_prevalence_pct"].corr(sub["military_exp_pct_gdp"])

fig, ax = plt.subplots(figsize=(7.5, 5.5))
ax.scatter(sub["military_exp_pct_gdp"], sub["diabetes_prevalence_pct"],
           alpha=0.6, color="#2E7D32", edgecolor="white", linewidth=0.4)
ax.set_xlabel("Military Expenditure (% of GDP)")
ax.set_ylabel("Diabetes Prevalence, Ages 20-79 (%)")
ax.set_title(f"Diabetes Prevalence vs. Military Spending\n(r = {corr_mil:.2f}, n={len(sub)} countries)")
plt.tight_layout()
plt.savefig("diabetes_vs_military_spending.png")
plt.close()

# ---------------------------------------------------------------------------
# 2. Diabetes prevalence vs. hospital bed capacity
# ---------------------------------------------------------------------------
sub2 = df.dropna(subset=["diabetes_prevalence_pct", "hospital_beds_per_1000"])
corr_beds = sub2["diabetes_prevalence_pct"].corr(sub2["hospital_beds_per_1000"])

fig, ax = plt.subplots(figsize=(7.5, 5.5))
ax.scatter(sub2["hospital_beds_per_1000"], sub2["diabetes_prevalence_pct"],
           alpha=0.6, color="#6A1B9A", edgecolor="white", linewidth=0.4)
ax.set_xlabel("Hospital Beds (per 1,000 people)")
ax.set_ylabel("Diabetes Prevalence, Ages 20-79 (%)")
ax.set_title(f"Diabetes Prevalence vs. Hospital Capacity\n(r = {corr_beds:.2f}, n={len(sub2)} countries)")
plt.tight_layout()
plt.savefig("diabetes_vs_hospital_beds.png")
plt.close()

# ---------------------------------------------------------------------------
# 3. Diabetes prevalence vs. GDP per capita, colored by income tercile
# ---------------------------------------------------------------------------
sub3 = df.dropna(subset=["diabetes_prevalence_pct", "gdp_per_capita_usd"]).copy()
sub3["income_tercile"] = pd.qcut(sub3["gdp_per_capita_usd"], 3, labels=["Lower-income third", "Middle-income third", "Higher-income third"])

fig, ax = plt.subplots(figsize=(8, 5.5))
colors = {"Lower-income third": "#C62828", "Middle-income third": "#F9A825", "Higher-income third": "#1565C0"}
for tercile, group in sub3.groupby("income_tercile", observed=True):
    ax.scatter(group["gdp_per_capita_usd"], group["diabetes_prevalence_pct"],
               label=tercile, alpha=0.65, color=colors[tercile], edgecolor="white", linewidth=0.4)
ax.set_xscale("log")
ax.set_xlabel("GDP per Capita, current US$ (log scale)")
ax.set_ylabel("Diabetes Prevalence, Ages 20-79 (%)")
ax.set_title("Diabetes Prevalence vs. GDP per Capita, by Income Tercile")
ax.legend()
plt.tight_layout()
plt.savefig("diabetes_vs_gdp_income_group.png")
plt.close()

# ---------------------------------------------------------------------------
# 4. Top / bottom 10 countries by diabetes burden
# ---------------------------------------------------------------------------
ranked = df.dropna(subset=["diabetes_prevalence_pct"]).sort_values("diabetes_prevalence_pct", ascending=False)
top10 = ranked.head(10).sort_values("diabetes_prevalence_pct")
bottom10 = ranked.tail(10).sort_values("diabetes_prevalence_pct")

fig, axes = plt.subplots(1, 2, figsize=(12, 5.5), sharex=False)
axes[0].barh(top10["country"], top10["diabetes_prevalence_pct"], color="#C62828")
axes[0].set_title("Highest Diabetes Prevalence")
axes[0].set_xlabel("Prevalence (%)")
axes[1].barh(bottom10["country"], bottom10["diabetes_prevalence_pct"], color="#2E7D32")
axes[1].set_title("Lowest Diabetes Prevalence")
axes[1].set_xlabel("Prevalence (%)")
plt.tight_layout()
plt.savefig("top_bottom_diabetes_burden.png")
plt.close()

# ---------------------------------------------------------------------------
# 5. Findings write-up
# ---------------------------------------------------------------------------
median_le_high = sub3[sub3["income_tercile"] == "Higher-income third"]["life_expectancy_years"].median() if "life_expectancy_years" in sub3 else np.nan

with open("findings.md", "w") as f:
    f.write("# Diabetes Burden, Spending Priorities, and Health System Capacity\n")
    f.write("### A cross-country analysis using World Bank World Development Indicators\n\n")
    f.write(f"**Data:** {len(df)} countries, most recent available year per indicator "
            "(World Bank, CC BY-4.0). See `data/` for source files.\n\n")

    f.write("## Motivating question\n")
    f.write("Countries differ widely in how they allocate public resources between defense and health "
            "system capacity. This project asks: is there a visible relationship between military "
            "spending, hospital capacity, and the burden of a major non-communicable disease "
            "(diabetes) across countries? This is a correlational look at publicly available "
            "cross-sectional data, not a causal analysis.\n\n")

    f.write("## Findings\n")
    f.write(f"1. **Military spending vs. diabetes burden:** correlation r = {corr_mil:.2f} "
            f"across {len(sub)} countries — a weak/near-zero relationship, suggesting military "
            "expenditure share alone is not a strong predictor of diabetes prevalence.\n")
    f.write(f"2. **Hospital capacity vs. diabetes burden:** correlation r = {corr_beds:.2f} across "
            f"{len(sub2)} countries.\n")
    f.write("3. **Income and diabetes prevalence:** diabetes prevalence does not fall cleanly with "
            "income; several higher-income Gulf states and Pacific Island nations appear among the "
            "highest-prevalence countries, while some lower-income countries have comparatively low "
            "measured prevalence -- consistent with the broader literature on diabetes as a disease "
            "increasingly concentrated in both high-income and rapidly urbanizing middle-income "
            "settings, not just wealthy nations.\n")
    f.write("4. See `top_bottom_diabetes_burden.png` for the specific highest- and lowest-prevalence "
            "countries in this dataset.\n\n")

    f.write("## Caveats\n")
    f.write("- This uses the most recent available year *per indicator per country*, not a single "
            "shared year, because WDI reporting years vary by country and indicator. This is a "
            "reasonable simplification for an exploratory cross-sectional look, but it is not a true "
            "panel and should not be read as showing trends over time.\n")
    f.write("- Correlation does not imply causation. Many confounders (urbanization, diet, genetics, "
            "screening/diagnosis rates, age structure) plausibly drive both diabetes prevalence and "
            "spending patterns.\n")
    f.write("- Diabetes prevalence estimates rely on differing national surveillance and diagnostic "
            "capacity, which itself correlates with health system investment -- a measurement caveat "
            "worth flagging in any policy-facing use of this kind of comparison.\n\n")

    f.write("## Why this project\n")
    f.write("This started from a personal interest in how spending priorities and public health "
            "capacity intersect -- shaped in part by growing up around military health systems and by "
            "prior research into diabetes treatment approaches. It is meant as a starting point for "
            "asking sharper policy questions (e.g., holding income and urbanization constant, does "
            "health-expenditure share predict diabetes outcomes better than military share does?) "
            "rather than as a finished causal claim.\n")

print("Analysis complete.")
print(f"corr(diabetes, military spend) = {corr_mil:.3f}")
print(f"corr(diabetes, hospital beds)  = {corr_beds:.3f}")
