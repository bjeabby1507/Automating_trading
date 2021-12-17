import requests
import json
import random

baseURL = "https://api.binance.com/api/v3/"

payload={}

# response = requests.request("GET", url, headers=headers, data=payload)
# print(response.text)

# get available crypto
def getdata():
    apiPrefix= "exchangeInfo"
    url = baseURL+apiPrefix
    response = requests.request("GET", url)
    response_json = json.loads(response.text)
    crypto = []
    #save the baseAsset an return the output list
    for key in response_json["symbols"]:
        data =key["baseAsset"]
        if data not in crypto :
            crypto.append(data)
    return crypto

def randomPair():
    apiPrefix= "exchangeInfo"
    url = baseURL+apiPrefix
    response = requests.request("GET", url)
    response_json = json.loads(response.text)
    crypto = []
    #save the baseAsset an return the output list
    for key in response_json["symbols"]:
        data =key["symbol"]
        if data not in crypto :
            crypto.append(data)
    return random.choice(crypto)

#display ask or bid
def getDepth(direction, pair):
    apiPrefix= "depth"
    url = baseURL+apiPrefix
    response = requests.request("GET", url, params=dict(symbol=pair))
    response_json = json.loads(response.text)
    #get the bids or ask
    direction_price=response_json[direction][0][0] #[price, volume]
    direction_volume=response_json[direction][0][1]
    return direction_price , direction_volume

def allgetDepth(direction, pair):
    apiPrefix= "depth"
    url = baseURL+apiPrefix
    response = requests.request("GET", url, params=dict(symbol=pair))
    response_json = json.loads(response.text)
    price = []
    #get the bids or ask price
    for key in response_json[direction] :
        price.append(key[0])
    return price

#get the order of an asset
def getOrder(pair):
    apiPrefix= "depth"
    url = baseURL+apiPrefix
    #print(url)
    response = requests.request("GET", url, params=dict(symbol=pair))
    response_json = json.loads(response.text)       
    return response_json

#read agegated trading data (candles)
def refreshDataCandle(pair , duration ):
    apiPrefix= "klines"
    url = baseURL+apiPrefix
    response = requests.request("GET", url, params=dict(symbol=pair,interval=duration))
    response_json = json.loads(response.text)       
    return response_json

"""
[
    1499040000000,      // Open time
    "0.01634790",       // Open
    "0.80000000",       // High
    "0.01575800",       // Low
    "0.01577100",       // Close
    "148976.11427815",  // Volume
    1499644799999,      // Close time
    "2434.19055334",    // Quote asset volume
    308,                // Number of trades
    "1756.87402397",    // Taker buy base asset volume
    "28.46694368",      // Taker buy quote asset volume
    "17928899.62484339" // Ignore. ]
    
SMA : Simple Moving Average : mean value across a period of n-previous observations
EMA : Exponential Moving Average : weighted mean across a period of n-previous observations where values closest to the most recent are given exponentially larger consideration
"""

def getDataCandle(pair , duration ):
    apiPrefix= "klines"
    url = baseURL+apiPrefix
    response = requests.request("GET", url, params=dict(symbol=pair,interval=duration))
    response_json = json.loads(response.text)
    key=['Open time','Open','High','Low','Close','Volume','Close time','Quote asset volume','Number of trades','Taker buy base asset volume','Taker buy quote asset volume','Ignore']
    #,'sma_7', 'ema_7','sma_30', 'ema_30' , 'sma_200' , 'ema_200'
    data =[]
    for datakey in response_json :
        sublist= datakey
        subdict = dict(zip(key,sublist))
        data.append(subdict)
    return data

#main
if __name__ == "__main__":
    crypto = getdata()
    #print(crypto)
    pairselected =randomPair()
    print(pairselected)
    #print('pair ',pairselected,' , bid ', getDepth(direction='bid',pair= pairselected))
    #print('pair ',pairselected,' , ask ', getDepth(direction='ask',pair= pairselected))
    #
    #print('pair ETHBTC, bid ',getDepth(direction='bids',pair= "ETHBTC"))
    price , volume = getDepth(direction='asks',pair= "ETHBTC")
    print('pair ETHBTC, ask ',getDepth(direction='asks',pair= "ETHBTC"))
    print('pair ETHBTC, ask ', " price "+ price, " volume "+ volume)
    #
    #print('pair ETHBTC, ask ',allgetDepth(direction='asks',pair= "ETHBTC"))
    #order = getOrder(pairselected)
    #print(order)
    #print('pair ETHBTC, Data candle ',refreshDataCandle(pair= "ETHBTC", duration='5m'))
    #print('pair ETHBTC, Data candle ',getDataCandle(pair= "ETHBTC", duration='5m'))