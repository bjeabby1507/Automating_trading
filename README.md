# Automating_trading

Binance api

- GET
  - getdata(): Get a list of all available cryptocurrencies and display it
  - getDepth(direction, pair) : function to display the ’ask’ or ‘bid’ price of an asset. Direction and asset name as parameters
  - getOrder(pair) : Get order book for an asset
  - refreshDataCandle(pair = 'BTCUSD', duration = '5m’) : function to read agregated trading data (candles)
  - Create a sqlite table to store said data (schema attached in the next slide)
    Store candlModify function to update when new candle data is available
    e data in the db
    StoreCandle(exchangeName,pair, duration): Store the candle  data in sqlite 
- POST
  - createOrder(api_key, api_secret, direction, price, amount, pair , orderType): Create an order
- DELETE
  - cancelOrder(api_key, api_secret, pair, uuid):Cancel an order