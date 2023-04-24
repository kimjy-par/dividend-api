import yfinance as yf
import pandas as pd

from datetime import datetime, timedelta

class Stock:
    def __init__(self, ticker_name):
        self.ticker = yf.Ticker(ticker_name)
        self.dividends = self.ticker.dividends
        self.dividends = pd.DataFrame(self.dividends).reset_index()
        self.dividends['Date'] = pd.to_datetime(self.dividends['Date']).dt.date

    def avg_growth(self):
        dividends = self.get_yearly_dividends()
        num_years = len(dividends)
        first_div = dividends[1].get('dividends')
        last_div = dividends[-2].get('dividends')

        div_growth = (last_div-first_div)/first_div
        avg_growth = div_growth/(num_years-2) * 100
         
        return avg_growth

    def get_first_and_last_year_of_dividends(self):
        first_dividends_date = str(self.dividends['Date'].iloc[0])
        first_dividends_date = datetime.strptime(first_dividends_date, '%Y-%m-%d')
        last_dividends_date = str(self.dividends['Date'].iloc[-1])
        last_dividends_date = datetime.strptime(last_dividends_date, '%Y-%m-%d')
        first_year = int(first_dividends_date.strftime('%Y'))
        last_year = int(last_dividends_date.strftime('%Y'))
        return first_year, last_year

    def get_dividends_from_range(self, start_date: datetime, end_date: datetime):
        start_date = datetime.date(start_date)
        end_date = datetime.date(end_date)
        total_dividends = self.dividends[(self.dividends['Date']>=start_date) & (self.dividends['Date']<=end_date)]\
                          ['Dividends'].sum()
        return total_dividends

    def get_yearly_dividends(self):
        first_year, last_year = self.get_first_and_last_year_of_dividends()
        yearly_dividends = [] 
        for year in range(first_year, last_year+1):
            prev_yearly_dividend = self.get_dividends_from_range(datetime(year-1,1,1), datetime(year-1,12,31))
            yearly_dividend = self.get_dividends_from_range(datetime(year,1,1), datetime(year,12,31))
            dividend_growth = (yearly_dividend-prev_yearly_dividend)/prev_yearly_dividend if prev_yearly_dividend!=0 else 0
            dividend_growth = dividend_growth * 100
            div_list = {
                'year': year,
                'dividends': yearly_dividend,
                'growth': dividend_growth
            }
            yearly_dividends.append(div_list)

        return yearly_dividends

    def print_yearly_dividends(self):
        dividends = self.get_yearly_dividends()
        for dividend in dividends:
            print(dividend)

    def get_last_dividends(self):
        pass

if __name__=="__main__":
    stock = Stock('SPHD')
    print(stock.dividends)
    yearly_dividends = stock.get_yearly_dividends()
    for dividend in yearly_dividends:
        print(dividend)
