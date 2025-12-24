from base_strategy import Strategy


class DemoStrategy(Strategy):
    def __init__(self, buy_threshold=0.003, sell_threshold=0.003):
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

    def decide(self, forecast, current_price, holding_qty):
        expected = forecast["expected_price"]

        if expected > current_price * (1 + self.buy_threshold):
            if holding_qty == 0:
                return "BUY"

        if expected < current_price * (1 - self.sell_threshold):
            if holding_qty > 0:
                return "SELL"

        return "HOLD"
