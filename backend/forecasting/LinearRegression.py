import numpy as np # type: ignore
from sklearn.linear_model import LinearRegression
from base_forecasting import BaseForecasting

class LinearRegressionForecasting(BaseForecasting):
    def __init__(self, symbol, bars):
        super().__init__(symbol, bars)
        self.model = LinearRegression()

    def train(self, X, y):
        self.model.fit(X, y)

    def predict_next(self, X, y):
        # predict next timestep
        next_t = [[len(X)]]
        self.expected_price = float(self.model.predict(next_t)[0])

        # R^2 as a simple confidence proxy
        self.confidence = float(self.model.score(X, y))

