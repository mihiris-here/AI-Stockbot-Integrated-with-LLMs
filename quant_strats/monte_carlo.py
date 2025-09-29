import numpy as np
import pandas as pd
from base_forecasting import BaseForecasting

class MonteCarlo(BaseForecasting):
    """
    Monte Carlo Simulation Strategy
    """

    def run_simulation(self):
        self.last_price = self.data['Close'].iloc[-1]
        all_simulations = []

        for _ in range(self.noOfSimulations):
            price_series = [self.last_price]
            for _ in range(1, self.noOfDays):
                price = price_series[-1] * (1 + np.random.normal(0, self.daily_volatility))
                price_series.append(price)

            all_simulations.append(price_series)

        # Store results as DataFrame
        self.simulation_df = pd.DataFrame(all_simulations).transpose()
