# Diabetes Burden, Spending Priorities, and Health System Capacity
### A cross-country analysis using World Bank World Development Indicators

**Data:** 209 countries, most recent available year per indicator (World Bank, CC BY-4.0). See `data/` for source files.

## Motivating question
Countries differ widely in how they allocate public resources between defense and health system capacity. This project asks: is there a visible relationship between military spending, hospital capacity, and the burden of a major non-communicable disease (diabetes) across countries? This is a correlational look at publicly available cross-sectional data, not a causal analysis.

## Findings
1. **Military spending vs. diabetes burden:** correlation r = 0.05 across 164 countries — a weak/near-zero relationship, suggesting military expenditure share alone is not a strong predictor of diabetes prevalence.
2. **Hospital capacity vs. diabetes burden:** correlation r = -0.07 across 200 countries.
3. **Income and diabetes prevalence:** diabetes prevalence does not fall cleanly with income; several higher-income Gulf states and Pacific Island nations appear among the highest-prevalence countries, while some lower-income countries have comparatively low measured prevalence -- consistent with the broader literature on diabetes as a disease increasingly concentrated in both high-income and rapidly urbanizing middle-income settings, not just wealthy nations.
4. See `top_bottom_diabetes_burden.png` for the specific highest- and lowest-prevalence countries in this dataset.

## Caveats
- This uses the most recent available year *per indicator per country*, not a single shared year, because WDI reporting years vary by country and indicator. This is a reasonable simplification for an exploratory cross-sectional look, but it is not a true panel and should not be read as showing trends over time.
- Correlation does not imply causation. Many confounders (urbanization, diet, genetics, screening/diagnosis rates, age structure) plausibly drive both diabetes prevalence and spending patterns.
- Diabetes prevalence estimates rely on differing national surveillance and diagnostic capacity, which itself correlates with health system investment -- a measurement caveat worth flagging in any policy-facing use of this kind of comparison.

## Why this project
This started from a personal interest in how spending priorities and public health capacity intersect -- shaped in part by growing up around military health systems and by prior research into diabetes treatment approaches. It is meant as a starting point for asking sharper policy questions (e.g., holding income and urbanization constant, does health-expenditure share predict diabetes outcomes better than military share does?) rather than as a finished causal claim.
