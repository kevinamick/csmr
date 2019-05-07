import pandas as pd
import pandas_datareader.data as web
from datetime import datetime
from concurrent import futures
import logging
import os

end = datetime.now()
start = datetime(end.year - 2, end.month, end.day)
logger = logging.getLogger(__name__)

def tickers():
	logger.debug("Saving tickers")
	data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	table = data[0]
	tickers = table.iloc[:, 0]
	return tickers


def download(ticker):
	data_feed = web.DataReader(ticker, "iex", start, end)
	
	try:
		path = f"{os.getcwd()}\\spy\\{ticker}.csv"
		data_feed.to_csv(path)
	except Exception as e: logger.error(e)

if __name__ == '__main__':
	logger.debug("Main")
	tickers = tickers()

	with futures.ThreadPoolExecutor(50) as executor:
		logger.debug("Starting threads")
		executor.map(download, tickers)

	logger.info("data import complete")
