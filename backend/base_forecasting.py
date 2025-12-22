import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import Dict


class BaseForecasting(ABC):
    """
    Abstract base class for all forecasting models.

    Responsibilities:
    - Accept market data from an external provider (Alpaca, CSV, etc.)
    - Perform common preprocessing (returns, volatility)
    - Enforce a standard forecast output contract
    """

    def __init__(self, symbol: str, historical_data: pd.DataFrame, horizon_days: int = 1):
        """
        Parameters
        ----------
        symbol : str
            Ticker symbol (e.g. AAPL)
        historical_data : pd.DataFrame
            Must contain columns: ['close']
            Indexed by datetime
        horizon_days : int
            How far ahead the forecast is (default: next day)
        """

        self.symbol = symbol
        self.horizon_days = horizon_days
        self.data = historical_data.copy()

        self._validate_data()
        self._preprocess()

        self.forecast_result: Dict = {}

    # ---------- Validation ----------

    def _validate_data(self):
        required_cols = {"close"}

        # Check if historical_data contains required columns
        if not required_cols.issubset(self.data.columns):
            raise ValueError(
                f"historical_data must contain columns: {required_cols}"
            )

        if len(self.data) < 20:
            raise ValueError("Not enough data for forecasting (min ~20 rows).")

    # ---------- Preprocessing ----------

    def _preprocess(self):
        """
        Shared preprocessing for all models.
        """
        self.data["log_return"] = np.log(
            self.data["close"] / self.data["close"].shift(1)
        )
        self.log_returns = self.data["log_return"].dropna()

        self.daily_volatility = self.log_returns.std()
        self.mean_return = self.log_returns.mean()

        self.last_price = float(self.data["close"].iloc[-1])

    # ---------- Forecasting ----------

    @abstractmethod
    def run(self):
        """
        Executes the forecasting model.
        Must set self.forecast_result.
        """
        pass

    def get_forecast(self) -> Dict:
        """
        Returns standardized forecast output.
        """
        if not self.forecast_result:
            raise RuntimeError("Forecast has not been run yet.")

        return self.forecast_result
