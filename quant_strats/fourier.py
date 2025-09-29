import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


class Fourier:
    def __init__(self, ticker, start_date, end_date, days):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.days = days  # number of harmonics to retain
        self.df = self.fetch_data()

    def fetch_data(self):
        df = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        df = df[['Adj Close']].dropna()
        df['Adj Close'] = df['Adj Close'] - df['Adj Close'].mean()  # center the data
        return df

    def apply_fft(self):
        close_prices = self.df['Adj Close'].values
        fft_result = np.fft.fft(close_prices)
        self.fft_result = fft_result
        return fft_result

    def filter_frequencies(self):
        fft_filtered = np.copy(self.fft_result)
        N = len(fft_filtered)
        fft_filtered[self.days+1:N-self.days] = 0  # keep top `days` frequencies
        return fft_filtered

    def inverse_fft(self, fft_filtered):
        reconstructed = np.fft.ifft(fft_filtered).real
        self.df['Reconstructed'] = reconstructed
        return reconstructed

    def plot(self):
        self.df.plot(title=f"Fourier Series Approximation for {self.ticker}")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.show()