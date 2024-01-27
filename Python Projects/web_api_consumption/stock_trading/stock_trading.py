"""
Dec, 2022
A project built for one of the Python courses I took at USU. This program calls an API with historical stock market prices in JSON format, 
then applies basic financial strategies (Simple Moving Average, Mean Reversion, and Bollinger Bands) to algorithmically "trade" the stocks, 
finally calculating the returns and results.
"""

import requests
import json
import time
import os

# this program does not currently work.

def create_data(tickers):
    for ticker in tickers:
        
        url = 'http://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+ticker+'&outputsize=full&apikey=NG9C9EPVYBMQT0C8'
        req = requests.get(url)
        input("pause")
        # time.sleep(12)
    
        req_dict = json.loads(req.text)
        
        time_key = "Time Series (Daily)"
        date_key = "2022-11-18"
        adj_close_key = "5. adjusted close"
        
        print(req_dict[time_key][date_key][adj_close_key])
        
        filepath = ''
        csv_fil = open(filepath + "/stock_trading/" + ticker + ".csv", "w")
        
        lst = []
        
        for date in req_dict[time_key]:
            print(req_dict[time_key][date][adj_close_key])
            
            lst.append(date + "," + req_dict[time_key][date][adj_close_key] + "\n")
        
        lst.reverse()
        
        for l in lst:
            csv_fil.write(l)
            
        csv_fil.close()
            
            
def append_data():
    for ticker in tickers:
        
        url = 'http://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+ticker+'&outputsize=full&apikey=NG9C9EPVYBMQT0C8'
        req = requests.get(url)
        # time.sleep(12)
    
        req_dict = json.loads(req.text)
        
        time_key = "Time Series (Daily)"
        date_key = "2022-11-18" # for example
        adj_close_key = "5. adjusted close"
        
        print(req_dict[time_key][date_key][adj_close_key])
        
        csv_fil = open(filepath + ticker + ".csv", "r")
        
        last_dt = csv_fil.readlines()[-1].split(",")[0]
        csv_fil.close
        
        lst = []
        
        for date in req_dict[time_key]:
            print(req_dict[time_key][date][adj_close_key])
            
            if date > last_dt:
                lst.append(date + "," + req_dict[time_key][date][adj_close_key] + "\n")
        
        lst.reverse()
        
        csv_fil = open(filepath + ticker + ".csv", "a")
        
        for l in lst:
            csv_fil.write(l)
            
        csv_fil.close()

    
#implement simple moving average strategy as a function that accepts a list of prices as an argument
def SimpleMovingAverage(prices):
    print(ticker, "Simple Moving Average Strategy Output:")
    i = 0
    buy = 0
    sell = 0
    position = 0
    tot_profit = 0
    start = 0
    
    for price in prices:
        
        if i >= 5: # 5 day moving average
            avg = ( prices[i-1] + prices[i-2] + prices[i-3] + prices[i-4] + prices[i-5] ) / 5
            if price > avg and position != 1:
                if i == len(prices) - 1:
                    print("buy this today! price is: ", price)
                else:
                    print("buying at: ", price)
                buy = price
                if start == 0:
                    start = price
                    first_pos = "bought"
                if sell != 0 and buy != 0:
                    tot_profit += sell - buy
                    print("trade profit: ", round(sell - buy, 2))
                position = 1
                
            elif price < avg and position != -1:
                if i == len(prices) - 1:
                    print("sell this today! price is: ", price)
                else:
                    print("selling at: ", price)
                sell = price
                if start == 0:
                    start = price
                    first_pos = "sold"
                if sell != 0 and buy != 0:
                    tot_profit += sell - buy
                    print("trade profit: ", round(sell - buy, 2))
                position = -1
            else:
                pass #do nothing
        i += 1
    
    #calculate returns
    print(start)
    returns = round((tot_profit / start) * 100,2)
    
    #return relevant results
    return round(tot_profit,2), start, first_pos, returns

#implement mean reversion strategy as a function that accepts a list of prices as an argument
def MeanReversionStrategy(prices):
    print(ticker, "Mean Reversion Strategy Output:")
    i = 0
    buy = 0
    sell = 0
    position = 0
    tot_profit = 0
    start = 0
    
    for price in prices:
        
        if i >= 5: # 5 day moving average
            avg = ( prices[i-1] + prices[i-2] + prices[i-3] + prices[i-4] + prices[i-5] ) / 5
            if price < (avg * 0.98) and position != 1:
                if i == len(prices) - 1:
                    print("buy this today! price is: ", price)
                else:
                    print("buying at: ", price)
                buy = price
                if start == 0:
                    start = price
                    first_pos = "bought"
                if sell != 0 and buy != 0:
                    tot_profit += sell - buy
                    print("trade profit: ", round(sell - buy, 2))
                position = 1
                
            elif price > (avg * 1.02) and position != -1:
                if i == len(prices) - 1:
                    print("sell this today! price is: ", price)
                else:
                    print("selling at: ", price)
                sell = price
                if start == 0:
                    start = price
                    first_pos = "sold"
                if sell != 0 and buy != 0:
                    tot_profit += sell - buy
                    print("trade profit: ", round(sell - buy, 2))
                position = -1
            else:
                pass #do nothing
        i += 1
    
    #calculate returns
    print(start)
    returns = round((tot_profit / start) * 100,2)
    
    #return relevant results
    return round(tot_profit,2), start, first_pos, returns
    
def BollingerBands(prices):
    print(ticker, "Bollinger Bands Strategy Output:")
    i = 0
    buy = 0
    sell = 0
    position = 0
    tot_profit = 0
    start = 0
    
    for price in prices:
        
        if i >= 5: # 5 day moving average
            avg = ( prices[i-1] + prices[i-2] + prices[i-3] + prices[i-4] + prices[i-5] ) / 5
            if price > (avg * 1.05) and position != 1:
                if i == len(prices) - 1:
                    print("buy this today! price is: ", price)
                else:
                    print("buying at: ", price)
                buy = price
                if start == 0:
                    start = price
                    first_pos = "bought"
                if sell != 0 and buy != 0:
                    tot_profit += sell - buy
                    print("trade profit: ", round(sell - buy, 2))
                position = 1
                
            elif price < (avg * 1.05) and position != -1:
                if i == len(prices) - 1:
                    print("sell this today! price is: ", price)
                else:
                    print("selling at: ", price)
                sell = price
                if start == 0:
                    start = price
                    first_pos = "sold"
                if sell != 0 and buy != 0:
                    tot_profit += sell - buy
                    print("trade profit: ", round(sell - buy, 2))
                position = -1
            else:
                pass #do nothing
        i += 1
    
    #calculate returns
    print(start)
    returns = round((tot_profit / start) * 100,2)
    
    #return relevant results
    return round(tot_profit,2), start, first_pos, returns

#save results to a new json file function
import json     
def SaveResults(results):
    json.dump(results, open(filepath + "/finalresults.json", "w"), indent = 4)
  
  
tickers = ["AAPL"] #"GOOG", "ADBE"] # "AMZN", "JBLU", "MCD", "MNST", "SPXL", "TQQQ", "TSLA"]

results = {}

create_data(tickers)

#iterate through each of the tickers in the list, recreating the prices list for each ticker
for ticker in tickers:
    
    prices = [round(float(line.split(",")[1]), 2) for line in open(filepath + "/stock_trading/" + ticker + ".csv", "r").readlines()]
    
    #print results from Simple Moving Average Strategy
    SMAprof, SMAfirstaction, SMAfirstpos, SMAreturns = SimpleMovingAverage(prices)
    print("------------------------------")
    print("Total Profit:", SMAprof)
    print("First Action:", SMAfirstpos, "at", SMAfirstaction)
    print("Percentage Returns:", SMAreturns, "%")
    print()
    
    #print results from Mean Reversion Strategy
    MRSprof, MRSfirstaction, MRSfirstpos, MRSreturns = MeanReversionStrategy(prices)
    print("------------------------------")
    print("Total Profit:", MRSprof)
    print("First Action:", MRSfirstpos, "at", MRSfirstaction)
    print("Percentage Returns:", MRSreturns, "%")
    print()
    
    #print results from Bollinger Bands Strategy
    BBprof, BBfirstaction, BBfirstpos, BBreturns = BollingerBands(prices)
    print("------------------------------")
    print("Total Profit:", BBprof)
    print("First Action:", BBfirstpos, "at", BBfirstaction)
    print("Percentage Returns:", BBreturns, "%")
    print()
    
    #fill out the dictionary with the results
    results[ticker + "_SMAprofit"] = SMAprof
    results[ticker + "_SMAreturns"] = SMAreturns
    results[ticker + "_MRSprofit"] = MRSprof
    results[ticker + "_MRSreturns"] = MRSreturns
    results[ticker + "_BBprofit"] = BBprof
    results[ticker + "_BBreturns"] = BBreturns
    
    #save results to a new json file
    SaveResults(results)
    
input("<PRESS ENTER>")
    
