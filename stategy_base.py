class Strategy:
    def __init__(self, data):
        self.data = data

    def generate_signals(self):
        raise NotImplementedError

    def backtest(self):
        raise NotImplementedError
