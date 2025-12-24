import pandas as pd # type: ignore
import numpy as np # type: ignore


class BaseForecasting:
    def __init__(self, symbol, bars):
        self.symbol = symbol
        self.bars = bars
        self.expected_price = None
        self.confidence = None

    def prepare_data(self):
        closes = np.array([b["close"] for b in self.bars])
        X = np.arange(len(closes)).reshape(-1, 1)
        y = closes
        return X, y

    def train(self, X, y):
        raise NotImplementedError

    def predict_next(self, X, y):
        raise NotImplementedError

    def run(self):
        X, y = self.prepare_data()
        self.train(X, y)
        self.predict_next(X, y)

    def get_forecast(self):
        return {
            "expected_price": self.expected_price,
            "confidence": self.confidence
        }