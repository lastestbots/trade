class CalculatorUtil:

    @staticmethod
    def position_profit(position, price):
        if position.price > 0:
            profit = (price - position.price) / position.price * 100
        elif position.price < 0:

            profit = 0 - (abs(position.price) - price) / abs(position.price) * 100
        else:
            profit = 0
        return profit
