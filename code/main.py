 
# Is diversification Time-Varying in Brazil? Evidence for a four years Index Bovespa

import pandas as pd
import numpy as np
from investpy import get_stock_historical_data, get_index_historical_data, get_stocks_list
from get_stocks_df import get_stock_dataframe


# Read the Index components
file_name = 'IBOV_carteira_setembro' + '.xlsx' 
theorical_portfolio = pd.read_excel(file_name)

data_stocks =  {'start_date': '01/01/2019',
				'country': ' brazil',
				'final_date':'21/10/2021' }


tickers_investpy = get_stocks_list(data_stocks.get('country'))

all_tickers = theorical_portfolio['Código'].tolist()

tickers_stock_list = [item for item in all_tickers if item in tickers_investpy]

filtered_theorical_portfolio = theorical_portfolio[theorical_portfolio['Código'].isin(tickers_stock_list)]

amount_assets = np.array([ filtered_theorical_portfolio['Qtde. Teórica'].tolist()])

total_theorical_amount =  amount_assets.sum()

weights_bovespa =  np.multiply(amount_assets,1/total_theorical_amount)

stocks_bovespa = get_stock_dataframe(tickers_list = tickers_stock_list,**data_stocks)

array_stocks = np.array(stocks_bovespa)

get_arithmetic_returns = lambda prices_array:  np.diff(prices_array, axis =0 ) / prices_array[ : -1]

returns = get_arithmetic_returns(array_stocks)

get_covariance = lambda returns_array: np.cov(returns_array.T)


diversification_index = lambda  volatilities,covariance,weights: np.dot(weights, volatilities.T)/ np.sqrt(np.dot(np.dot(weights,covariance.T),weights.T))

bovespa = get_index_historical_data('Bovespa', from_date = '01/01/2019', to_date = '21/10/2021', country = 'brazil')

def rolling_diversification(returns_array,weights):

	days_rolling = 21
	diversification_rolling = [] ; index = []
	size_array = returns_array.shape[0]

	for i in range(days_rolling,size_array,days_rolling):
		covariance = get_covariance(returns_array[i-days_rolling:i])  
		vol_stocks = np.array([np.diag(covariance)])

		div_index = diversification_index(vol_stocks,covariance,weights)
		index.append(i); diversification_rolling.append(div_index[0][0])

	return index, diversification_rolling


date_index_diversification,ratio_diversification = rolling_diversification(returns,weights_bovespa) 

date_index = [stocks_bovespa.index.tolist()[i] for i in date_index_diversification]

ratio_df = pd.DataFrame({'Date':date_index, 'Ratio_diversification':ratio_diversification})




