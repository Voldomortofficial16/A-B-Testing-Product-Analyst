# A-B-Testing-Product-Analyst
Created A/B Testing Model
# A/B Testing Experiment Report

## Objective

Evaluate whether Version B improves Click-Through Rate (CTR) compared to Version A.

## Overall Results

Version B achieved a CTR of 12.63% compared to 10.22% for Version A, representing a 23.55% relative uplift.

A two-proportion Z-test produced a p-value of 0.000153, indicating that the observed improvement is statistically significant at the 95% confidence level.

## Country-Level Analysis

Version B showed statistically significant improvements across all evaluated countries:

* USA (p = 0.0362)
* India (p = 0.0180)
* UK (p = 0.0197)

This suggests that the treatment effect is consistent across geographies.

## Device-Level Analysis

* Mobile: Significant improvement (p = 0.0003)
* Tablet: Significant improvement (p = 0.0421)
* Desktop: No significant difference (p = 0.7876)

The majority of the overall uplift appears to be driven by Mobile users.

## Recommendation

Deploy Version B globally for Mobile and Tablet users.

Further investigation is recommended before deploying Version B exclusively for Desktop users, as no statistically significant improvement was observed in that segment.
