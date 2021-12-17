import requests
import json
import sqlite3
import os
import time
import hmac
import hashlib
import db
from urllib.parse import urlencode
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

Api_key= os.environ.get("API_KEY")
Api_secret= os.environ.get("API_SECRET")
API_URL = 'https://testnet.binance.vision/api/v3/'

headers = {
    'X-MBX-APIKEY': Api_key
}
#Bianace API Trade : API key and signature
#Create an order
def createOrder(api_key, api_secret, direction, price, amount, pair , orderType):
    apiPrefix= "order"
    url = API_URL+apiPrefix
    headers = {
    'X-MBX-APIKEY': api_key
    }
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': pair,
        'side': direction,
        'type': orderType,
        'timeInForce': 'GTC',
        'quantity': amount,
        'price': price,
        'timestamp': timestamp
    }

    query_string = urlencode(params)
    params['signature'] = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    response = requests.post(url, headers=headers, params=params)
    response_json = json.loads(response.text)
    print(response_json)
    
    #save to DB
    db.OrderDB('Bianace',pair)
    setTableName = str('Bianace' + "_" + pair)
    conn = sqlite3.connect('order_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO "+ setTableName + " VALUES (null,?,?,?,?,?)",(response_json['orderId'],response_json['origQty'],response_json['price'],response_json['transactTime'],response_json['side']))
    conn.commit()
    c.execute('SELECT * FROM '+ setTableName)
    setTableName = c.fetchall()
    for row in setTableName :
        print (row)
    conn.close()
    
    return response_json

#Cancel an order
def cancelOrder(api_key, api_secret, pair, uuid):
    apiPrefix= "order"
    url = API_URL+apiPrefix
    headers = {
    'X-MBX-APIKEY': api_key
    }
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': pair,
        'orderId': uuid,
        'timestamp': timestamp
    }

    query_string = urlencode(params)
    params['signature'] = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    response = requests.delete(url, headers=headers, params=params)
    response_json = json.loads(response.text)
    
    #remove from DB
    setTableName = str('Bianace' + "_" + pair)
    conn = sqlite3.connect('order_database.db')
    c = conn.cursor()
    c.execute("DELETE FROM "+ setTableName + " WHERE uuid = " + str(uuid))
    conn.commit()
    c.execute('SELECT * FROM '+ setTableName)
    setTableName = c.fetchall()
    for row in setTableName :
        print (row)
    conn.close()
    
    return response_json

def getOrder(pair):
    apiPrefix= "depth"
    url = API_URL+apiPrefix
    #print(url)
    response = requests.request("GET", url, params=dict(symbol=pair))
    response_json = json.loads(response.text)       
    return response_json

#main
if __name__ == "__main__":
    ## Order
    #print(getOrder("ETHBTC"))
    #order= createOrder(Api_key,Api_secret, direction='BUY', price=0.08077800 ,amount=0.01000000, pair = 'ETHBTC', orderType = 'LIMIT')
    #{'symbol': 'ETHBTC', 'orderId': 2465, 'orderListId': -1, 'clientOrderId': 'K8tpMxNGzjzJQJssfqXj1x', 'transactTime': 1639699887114, 'price': '0.08077800', 'origQty': '0.01000000',
    # 'executedQty': '0.00000000', 'cummulativeQuoteQty': '0.00000000', 'status': 'NEW', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'BUY', 'fills': []}
    
    #check DB
    conn = sqlite3.connect('order_database.db')
    c = conn.cursor()
    setTableName = str('Bianace' + "_" + 'ETHBTC')
    c.execute('SELECT * FROM '+ setTableName)
    setTableName = c.fetchall()
    for row in setTableName :
        print (row)
    conn.close()
    #(1, '2465', 0.01, 0.080778, 1639699887114, 'BUY')
    
    #Cancel
    #cancelOrder(Api_key, Api_secret, pair= 'ETHBTC', uuid=2465)