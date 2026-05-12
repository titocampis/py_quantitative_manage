# Quantitative Data Manager with Python Statistics 📈🤓

Welcome to Quantitative Data Manager with Python Stadistic!

You just have to import your data into a csv in the file: [dades.csv](dades.csv) and enjoy 🚀🚀🚀🚀

## Statistical Interpretation Guide

### Spearman Correlation (ρ)

| ρ | Interpretation |
|------------|----------------|
| ρ < .2 | very weak / negligible correlation |
| .2 ≤ ρ < .4 | weak correlation |
| .4 ≤ ρ < .6 | moderate correlation |
| .6 ≤ ρ < .8 | strong correlation |
| ρ ≥ .8 | very strong correlation |

### p-value (Spearman)

| p-value | Interpretation |
|---------------|----------------|
| p < .001 | very strong statistical significance (very strong evidence against the null hypothesis) |
| .001 ≤ p < .01 | strong statistical significance (strong evidence against the null hypothesis) |
| .01 ≤ p < .05 | statistical significance (evidence against the null hypothesis) |
| p ≥ .05 | not statistically significant (insufficient evidence to reject the null hypothesis) |

---

### Chi-square (χ²) Test of Independence

| Element | Interpretation |
|----------|----------------|
| χ² statistic | Measures the discrepancy between the observed frequencies and the expected frequencies if the variables were independent. Doesn't indicate strength directly (depends on sample size and degrees of freedom). Interpretation is based on p-value and effect size (Cramér’s V). |

### p-value (χ² test)

| p-value | Interpretation |
|---------------|----------------|
| p < .001 | very strong statistical significance (very strong evidence of association; reject the null hypothesis) |
| .001 ≤ p < .01 | strong statistical significance (strong evidence of association; reject the null hypothesis) |
| .01 ≤ p < .05 | statistical significance (evidence of association; reject the null hypothesis) |
| p ≥ .05 | not statistically significant (insufficient evidence to conclude association; fail to reject the null hypothesis) |

### Cramér’s V (effect size for χ²)

\[
V = \sqrt{\frac{\chi^2}{n \cdot (k - 1)}}
\]

- **χ²** → chi-square statistic  
- **n** → total sample size  
- **k** → \[
k = \min(\text{rows}, \text{columns})
\]

| Range of V | Interpretation |
|------------|----------------|
| V < .10 | negligible association |
| .10 ≤ V < .30 | weak association |
| .30 ≤ V < .50 | moderate association |
| V ≥ .50 | strong association |
