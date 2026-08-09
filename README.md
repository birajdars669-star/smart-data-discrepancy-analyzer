# Smart Data Discrepancy Analyzer

## Automated Comparison, Root-Cause Identification and Impact Estimation Across Data Sources

Smart Data Discrepancy Analyzer is a Python and Streamlit-based analytical application designed to compare two structured transactional data sources and identify discrepancies between them.

The system detects missing records and order-level metric differences, identifies potential root causes, and estimates the financial impact associated with the detected discrepancies.

## Key Features

- Automated comparison of two transactional data sources
- Detection of missing records
- Identification of quantity mismatches
- Identification of price mismatches
- Order-level sales comparison
- Automated root-cause identification
- Financial impact estimation
- Date-range validation
- Interactive Streamlit dashboard
- Test datasets for validation

## Problem Statement

When the same business data is maintained across multiple sources, discrepancies can occur due to missing records, inconsistent quantities, different prices, or other data inconsistencies.

Manually identifying the cause of these differences can be time-consuming and may make it difficult to understand the actual business impact.

This project provides an automated approach for detecting and analyzing such discrepancies.

## How It Works

1. Upload Source A and Source B transactional datasets.
2. The system validates the uploaded data.
3. Records are compared using the order identifier.
4. Missing records are detected.
5. Order-level quantity and price differences are identified.
6. Potential root causes are assigned.
7. The impact of each discrepancy is calculated.
8. The application displays the main root cause and estimated overall impact.

## Technology Stack

- Python
- Pandas
- Streamlit
- CSV datasets

## Project Structure

```text
smart-data-discrepancy-analyzer/
│
├── app.py
├── app_causal_impact.py
├── main.py
├── test_streamlit.py
├── test_a.csv
├── test_b.csv
├── Patent_Documentation_Smart_Causal_Impact_Analyzer.docx
└── README.md
## Patent / Innovation Overview

This project is developed as a technical prototype for a patent-oriented innovation in automated data discrepancy analysis.

The proposed approach combines:
- Source-level metric comparison
- Transaction-level discrepancy detection
- Attribute-level root-cause identification
- Estimated financial impact analysis
- Actionable analytical reporting

The system is designed to help users understand not only that two data sources differ, but also where the discrepancy occurs, what may have caused it, and its estimated impact.

## Evidence and Documentation

The repository includes:
- Patent-oriented technical documentation
- Prior-art comparison and differentiation
- Draft patent claims
- Application screenshots
- Screen recording
- Test CSV datasets
