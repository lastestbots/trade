class CalculatorUtil:

    @staticmethod
    def position_profit(position, price):
        """
        计算仓位利润
        :param position:
        :param price:
        :return:
        """

        if position.size > 0:
            profit = (price - position.price) / position.price * 100
        elif position.size < 0:

            profit = (position.price - price) / position.price * 100
        else:
            profit = 0
        return profit
