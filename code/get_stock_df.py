import pandas as pd
import numpy as np
from investpy import get_stock_historical_data, get_index_historical_data, get_stocks_list

def get_stock_dataframe(tickers_list, **kwargs):
	stocks_list = []

	stocks_dfs = pd.DataFrame()


	start_date = kwargs.get('start_date')

	final_date = kwargs.get('final_date')

	country = kwargs.get('country')

	bovespa = get_index_historical_data('Bovespa', from_date = start_date, to_date =  final_date, country = country)

	start_date_index = bovespa.index[0]


	for ticker in tickers_list:

		stock_price = get_stock_historical_data( stock = ticker, from_date = start_date, to_date =  final_date, country = country)

		if stock_price.index[0] != start_date_index:

			stock_price =  bovespa

		stocks_dfs[ticker] = stock_price['Close']
		 

	return stocks_dfs.dropna()