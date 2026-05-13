# TFM Hàbits lectors de l'alumnat de 3r d'ESO fins a 2n de Batxillerat en un centre educatiu de l’Hospitalet de Llobregat. 

## How to use the python scripts to run data analysis for the TFM?

:one: Access the directory python

:two: Run the command main with the desired tag:
- -v: verbosity
- -t #: to perform the different tasks
```bash
main.py [-v] [-t 9] 
```

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

### Contingency Table Example
Contingency table is the cross-tabulation of two categorical variables that shows the frequency of each combination of categories.

|       | 0 min | <30 min | 1–2 h | ... |
|-------|-------|---------|-------|-----|
| Noies | 50    | 20      | 10    | ... |
| Nois  | 70    | 25      | 5     | ... |

### Cramér’s V (effect size for χ²)

```
V = sqrt(chi2 / (n * (k - 1)))
```
- **χ²** → chi-square statistic obtained from the contingency table  
- **n** → total sample size used in the contingency table  
  `n = contingency_table.sum().sum()`  
- **k** → number of categories considered in the test  
  `k = min(contingency_table.shape)`

| Range of V | Interpretation |
|------------|----------------|
| V < .1 | negligible association |
| .1 ≤ V < .3 | weak association |
| .3 ≤ V < .5 | moderate association |
| V ≥ .5 | strong association |
