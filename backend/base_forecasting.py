import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

class BaseForecasting(ABC):
    """
    Abstract Base Class for forecasting strategies (Monte Carlo, Fourier, Brownian, etc.)
    Provides common functionality like data loading, log returns, volatility,
    plotting, and result interpretation.
    """

    def __init__(self, ticker, start_date, end_date, days, sim=100):
        self.ticker = ticker
        self.start = start_date
        self.end = end_date
        self.noOfSimulations = sim
        self.noOfDays = days

        self.import_stock_data()
        self.calc_log_returns()
        self.volatility_calc()

    def import_stock_data(self):
        stock = yf.Ticker(self.ticker)
        self.data = stock.history(start=self.start, end=self.end)

    def calc_log_returns(self):
        # Assuming the 'Close' prices
        self.log_returns = np.log(1 + self.data['Close'].pct_change()).dropna()

    def volatility_calc(self):
        # Standard deviation will be used for volatility
        self.daily_volatility = np.std(self.log_returns)

    @abstractmethod
    def run_simulation(self):
        """
        Abstract method for running the forecasting strategy.
        Each subclass must implement this (Monte Carlo, Fourier, etc.).
        """
        pass

    def results(self):
        prices = self.simulation_df.iloc[-1]  # last day prices from all simulations
        lower_bound = np.percentile(prices, 2.5)
        upper_bound = np.percentile(prices, 97.5)
        mean_price = np.mean(prices)


    def plot(self):
        pass