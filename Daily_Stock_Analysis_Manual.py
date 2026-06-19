import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ta.momentum import RSIIndicator
from ta.trend import MACD
import os

#C:\Users\lucif\Downloads\NEWPORTFOLIO.xlsx
file_directory = "C:/Users/lucif/Desktop/Studia/Analiza Finansowa Własna/Stocks/Daily Stock Analysis/Daily_Stocks — TEST.xlsx"


def fetch_stock_data(file_path, days):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found. Please check the path.")

    try:
        data = pd.read_excel(file_path, parse_dates=['Date'], index_col='Date')
    except Exception as e:
        raise ValueError(f"Error reading Excel file: {e}. Ensure it has a 'Date' column and valid data.")

    if data.empty or len(data.columns) < 1:
        raise ValueError("Excel file is empty or has no data columns.")

    data = data.sort_index()

    # --- POPRAWKA: Dynamiczne określanie zakresu na podstawie danych ---
    # Szukamy najświeższej daty fizycznie istniejącej w pliku Excel
    end_date = data.index.max()
    start_date = end_date - pd.Timedelta(days=days)

    print(f"📊 Loading data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}...")
    data = data.loc[start_date:end_date]

    if data.empty:
        raise ValueError(
            f"No data available in the specified period ({days} days). Check the date range in the Excel file.")

    return data

def calculate_metrics(data, days, sma_short=10, sma_long=50, market_column=None):
    results = []
    log_returns = np.log(data / data.shift(1))

    sma_short_series_all = {}
    sma_long_series_all = {}
    rsi_all = {}
    macd_lines = {}
    signal_lines = {}

    betas = {}
    if market_column and market_column in data.columns:
        betas = calculate_beta(log_returns, market_column)

    for ticker in data.columns:
        volatility = log_returns[ticker].std() * np.sqrt(252)
        mean_log_return = log_returns[ticker].mean() * 252
        volatility_of_returns = log_returns[ticker].rolling(window=10).std() * np.sqrt(252)
        mean_volatility_of_returns = volatility_of_returns.mean() if not volatility_of_returns.empty else np.nan

        # SMA
        sma_short_series_all[ticker] = data[ticker].rolling(window=sma_short).mean()
        sma_long_series_all[ticker] = data[ticker].rolling(window=sma_long).mean()

        # RSI
        rsi_series = RSIIndicator(data[ticker], window=14).rsi()
        rsi_all[ticker] = rsi_series

        # MACD
        macd = MACD(data[ticker], window_slow=26, window_fast=12, window_sign=9)
        macd_line = macd.macd()
        signal_line = macd.macd_signal()

        macd_lines[ticker] = macd_line
        signal_lines[ticker] = signal_line

        latest_rsi = rsi_series.iloc[-1] if not rsi_series.empty else np.nan
        latest_macd = macd_line.iloc[-1] if not macd_line.empty else np.nan
        latest_signal = signal_line.iloc[-1] if not signal_line.empty else np.nan

        results.append({
            'Ticker': ticker,
            'Mean Log Return (Annualized)': mean_log_return,
            'Volatility (Annualized)': volatility,
            'Mean Volatility of Returns': mean_volatility_of_returns,
            'Latest RSI': latest_rsi,
            'Latest MACD': latest_macd,
            'Latest Signal Line': latest_signal,
            'Beta vs Market': betas.get(ticker, np.nan) if betas else np.nan
        })

    results_df = pd.DataFrame(results)
    correlation_matrix = log_returns.corr()

    return results_df, correlation_matrix, data, log_returns, sma_short_series_all, sma_long_series_all, rsi_all, macd_lines, signal_lines

#BETA
def calculate_beta(log_returns,market_column):
    betas = {}
    market_returns = log_returns[market_column].dropna()

    for ticker in log_returns.columns:
        if ticker == market_column:
            continue

        combined = pd.concat([log_returns[ticker], market_returns], axis=1).dropna()
        Ri = combined.iloc[:, 0]
        Rm = combined.iloc[:, 1]

        covariance = np.cov(Ri, Rm)[0][1]
        variance = np.var(Rm)
        beta = covariance/variance if variance !=0 else np.nan
        betas[ticker] = beta
    return betas
    print(betas)

def plot_stock_data(data, log_returns, sma_short_series_all, sma_long_series_all, rsi_all, macd_lines, signal_lines, tickers):
    for ticker in tickers:
        if ticker not in data.columns:
            continue

        plt.figure(figsize=(12, 8))
        plt.subplot(3, 1, 1)
        plt.plot(data.index, data[ticker], label=f'{ticker} Price')
        plt.plot(data.index, sma_short_series_all[ticker], label=f'{ticker} {10}-day SMA')
        plt.plot(data.index, sma_long_series_all[ticker], label=f'{ticker} {50}-day SMA')
        plt.title(f'{ticker} Price and Moving Averages')
        plt.legend()

        plt.subplot(3, 1, 2)
        plt.plot(log_returns.index, log_returns[ticker], label=f'{ticker} Log Returns')
        plt.title(f'{ticker} Log Returns')
        plt.legend()

        plt.subplot(3, 1, 3)
        plt.plot(rsi_all[ticker].index, rsi_all[ticker], label='RSI', color='purple')
        plt.axhline(70, linestyle='--', alpha=0.5, color='red')
        plt.axhline(30, linestyle='--', alpha=0.5, color='green')
        plt.title(f'{ticker} RSI')
        plt.legend()

        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(12, 4))
        plt.plot(macd_lines[ticker].index, macd_lines[ticker], label='MACD', color='blue')
        plt.plot(signal_lines[ticker].index, signal_lines[ticker], label='Signal Line', color='orange')
        plt.title(f'{ticker} MACD')
        plt.legend()
        plt.show()


def main():
    # Pobierz liczbę dni od użytkownika
    while True:
        try:
            days = int(input("Enter number of days for analysis (e.g., 90): "))
            if days <= 0:
                raise ValueError("Number of days must be positive.")
            break
        except ValueError:
            print("Please enter a valid positive integer for days.")

    # Wczytaj dane z pliku Excel
    try:
        data = fetch_stock_data(file_directory, days)
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    market_column = input("Enter name of index: ")

    tickers = data.columns.tolist()

    results_df, correlation_matrix, data, log_returns, sma_short_series_all, sma_long_series_all, rsi_all, macd_lines, signal_lines = calculate_metrics(
        data, days, market_column=market_column
    )

    print("\nStock Analysis Results:")
    print(results_df.to_string(index=False))

    print("\nCorrelation Matrix:")
    print(correlation_matrix)

    plot_stock_data(data, log_returns, sma_short_series_all, sma_long_series_all, rsi_all, macd_lines, signal_lines,
                    tickers)

    results_df.to_csv('stock_analysis_results.csv', index=False)
    correlation_matrix.to_csv('correlation_matrix.csv')

    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Matrix of Stock Returns')
    plt.show()

if __name__ == "__main__":
    main()
