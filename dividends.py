import yfinance as yf
import pandas as pd

from datetime import datetime, timedelta

class Stock:
    def __init__(self, ticker_name):
        self.ticker = yf.Ticker(ticker_name)
        self.dividends = self.ticker.dividends

    def get_first_and_last_year_of_dividends(self):
        dividends = pd.DataFrame(self.dividends).reset_index()
        first_dividends_date = str(dividends['Date'].iloc[0])
        first_dividends_date = datetime.strptime(first_dividends_date, '%Y-%m-%d %H:%M:%S')
        last_dividends_date = str(dividends['Date'].iloc[-1])
        last_dividends_date = datetime.strptime(last_dividends_date, '%Y-%m-%d %H:%M:%S')
        first_year = int(first_dividends_date.strftime('%Y'))
        last_year = int(last_dividends_date.strftime('%Y'))
        return first_year, last_year

    def get_dividends_from_range(self, start_date: datetime, end_date: datetime):
        dividends = pd.DataFrame(self.dividends).reset_index()
        total_dividends = dividends[(dividends['Date']>=start_date) & (dividends['Date']<=end_date)]\
                          ['Dividends'].sum()
        return total_dividends

    def get_yearly_dividends(self):
        first_year, last_year = self.get_first_and_last_year_of_dividends()
        yearly_dividends = [] 
        for year in range(first_year, last_year+1):
            prev_yearly_dividend = self.get_dividends_from_range(datetime(year-1,1,1), datetime(year-1,12,31))
            yearly_dividend = self.get_dividends_from_range(datetime(year,1,1), datetime(year,12,31))
            dividend_growth = (yearly_dividend-prev_yearly_dividend)/prev_yearly_dividend if prev_yearly_dividend!=0 else 0
            div_list = {
                'year': year,
                'dividends': yearly_dividend,
                'growth': dividend_growth
            }
            yearly_dividends.append(div_list)

        return yearly_dividends

    def get_last_dividends(self):
        pass

if __name__=="__main__":
    stock = Stock('SPHD')
    yearly_dividends = stock.get_yearly_dividends()
    for dividend in yearly_dividends:
        print(dividend)