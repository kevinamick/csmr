import import_data
from CrossSectionalMRStrategy import CrossSectionalMR
import os
import backtrader as bt
import logging
import sys
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (10, 6) # (w, h)
plt.ioff()

cerebro = bt.Cerebro()
cerebro.broker.set_coc(True)
logger = logging.getLogger(__name__)

def main():
    logger.debug("Starting BackTest")
    for ticker in os.listdir("spy"):
        data = bt.feeds.GenericCSVData(
            fromdate=import_data.start,
            todate=import_data.end,
            dataname=f"spy/{ticker}",
            dtformat='%Y-%m-%d',
            openinterest=-1,
            nullvalue=0.0,
            plot=False
        )
        cerebro.adddata(data)

    cerebro.broker.setcash(1_000_000)
    cerebro.addobserver(bt.observers.Value)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, riskfreerate=0.0)
    cerebro.addanalyzer(bt.analyzers.Returns)
    cerebro.addanalyzer(bt.analyzers.DrawDown)
    cerebro.addstrategy(CrossSectionalMR)

    logger.debug("Running BackTest")
    results = cerebro.run()

    logger.info(f"Sharpe: {results[0].analyzers.sharperatio.get_analysis()['sharperatio']:.3f}")
    logger.info(f"Norm. Annual Return: {results[0].analyzers.returns.get_analysis()['rnorm100']:.2f}%")
    logger.info(f"Max Drawdown: {results[0].analyzers.drawdown.get_analysis()['max']['drawdown']:.2f}%")
    cerebro.plot()[0][0]


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    main()
