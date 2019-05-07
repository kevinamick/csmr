import backtrader as bt
import numpy as np


class CrossSectionalMR(bt.Strategy):

    def prenext(self):
        self.next()

    def next(self):
        available = list(filter(lambda data: len(data), self.datas))

        avg_daily_returns = np.zeros(len(available))
        for i, d in enumerate(available):
            beginning_period_return = d.close[0]
            end_period_return = d.close[-1]
            avg_daily_returns[i] = (beginning_period_return - end_period_return) / end_period_return

        market_mean_returns = np.mean(avg_daily_returns)
        weights = -(avg_daily_returns - market_mean_returns)
        weights = weights / np.sum(np.abs(weights))

        for i, d in enumerate(available):
            self.order_target_percent(d, target=weights[i])
