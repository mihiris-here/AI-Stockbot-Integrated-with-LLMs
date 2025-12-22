class Strategy:
    def __init__(self, data):
        self.data = data
    
    def decide(self, forecast, current_price, holdings):
        raise NotImplementedError

    def generate_signals(self):
        raise NotImplementedError

    def backtest(self):
        raise NotImplementedError
