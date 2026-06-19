# Quantitative & Technical Stock Analyzer (Local Data Engine)

## Overview
This repository contains a standalone **Technical & Statistical Stock Analysis Terminal** built in Python. Designed as a robust alternative to unstable financial market APIs, this tool performs comprehensive quantitative analysis directly on historical price data stored in local Excel spreadsheets.

The script filters data dynamically based on user input, processes logarithmic returns, and combines **academic risk metrics (Modern Portfolio Theory baseline)** with **classic technical analysis indicators** to deliver actionable market insights.

---

## Key Features

* **API-Independent Ingestion:** Reads directly from local `.xlsx` files, automatically adapting to the latest available historical date in the dataset.
* **Quantitative Risk Metrics:** Annualizes returns and volatility, and evaluates asset sensitivity against a benchmark (Beta).
* **Technical Analysis Suite:** Implements trend and momentum oscillators using the `ta` library.
* **Automated Data Export:** Saves analytical outputs and cross-asset relationships to `.csv` files for further research or reporting.
* **Multi-Frame Visualization:** Generates dedicated technical charts (Price, SMAs, Log Returns, RSI, MACD) and correlation heatmaps for every ticker.

---

## Core Metrics & Financial Indicators Explained

### 1. Statistical & Risk Metrics
* **Mean Log Return (Annualized):** Represents the expected continuous growth rate of an asset over a one-year horizon based on the analyzed window.
* **Volatility (Annualized):** Calculated as the annualized standard deviation of log returns ($\sigma \times \sqrt{252}$), serving as the primary measure of market risk.
* **Mean Volatility of Returns:** Captures short-term risk dynamics using a 10-day rolling window approach.
* **Beta vs Market ($\beta$):** Measures the systematic risk or volatility of an asset relative to a user-defined market index (e.g., WIG20, WIG30, S&P500). 
  $$\beta = \frac{\text{Covariance}(R_i, R_m)}{\text{Variance}(R_m)}$$

### 2. Technical Analysis Indicators
* **Simple Moving Averages (SMA):** Employs a short-term (10-day) and long-term (50-day) SMA overlay to visually identify trend reversals, support/resistance lines, and potential entry/exit signals.
* **Relative Strength Index (RSI):** A 14-day momentum oscillator bounded between 0 and 100. Horizontal thresholds are fixed at **30** (oversold conditions / buy signal baseline) and **70** (overbought conditions / sell signal baseline).
* **MACD (Moving Average Convergence Divergence):** Computes the difference between the 26-day and 12-day exponential moving averages, plotted alongside a 9-day Signal Line to signal shifting momentum.

---

## Project Structure & Outputs

### Input Requirements
The system expects an Excel file (`.xlsx`) structured with a `'Date'` index column and asset closing prices as subsequent columns. 

### Generated Outputs
1. **Terminal Report:** A structured, real-time summary dataframe displaying the latest computed technical and statistical values for all assets.
2. **`stock_analysis_results.csv`:** Tabular file containing all metrics for seamless integration into Excel or thesis documentation.
3. **`correlation_matrix.csv`:** Raw correlation coefficients representing how assets move relative to each other.
4. **Visualizations:** * Interactive multi-panel charts for individual stock evaluation.
   * A clean **Seaborn Correlation Heatmap** to assess portfolio diversification potential.

---

## Getting Started

### Installation
Ensure you have the required dependencies installed:
```bash
pip install pandas numpy matplotlib seaborn ta openpyxl
