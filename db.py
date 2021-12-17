import sqlite3
import test
import datetime 

dt = datetime.datetime.now()
seq = int(dt.strftime("%Y%m%d%H%M%S"))

#create candle Table from

def createDB(exchangeName,pair,duration):
    setTableName = str(exchangeName + "_" + pair + "_" + duration)
    conn = sqlite3.connect('test_database.db')
    c = conn.cursor()
    tableCreationStatement = """CREATE TABLE IF NOT EXISTS """ + setTableName + """(Id INTEGER PRIMARY KEY, date INT UNIQUE, high REAL, low REAL, open REAL, close REAL, volume REAL, quotevolume REAL)"""
    c.execute(tableCreationStatement)
    conn.commit()
    conn.close()

    
def trackUpdateDB():
    conn = sqlite3.connect('track_database.db')
    c = conn.cursor()
    tableCreationStatement = """CREATE TABLE IF NOT EXISTS last_checks(Id INTEGER PRIMARY KEY, exchange TEXT, trading_pair TEXT, duration TEXT, table_name TEXT, last_check INT, startdate INT, last_id INT,UNIQUE(table_name,last_check))"""
    c.execute(tableCreationStatement)
    conn.commit()
    conn.close()

def track(exchangeName,pair,duration):
    setTableName = str(exchangeName + "_" + pair + "_" + duration)
    conn = sqlite3.connect('test_database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM '+ setTableName + ' WHERE Id = (SELECT MAX(Id) FROM '+ setTableName +')')
    ALL = c.fetchone()
    print("All", ALL)
    last_id = ALL[0]
    last_check = ALL[1]
    
    conn2 = sqlite3.connect('track_database.db')
    c2 = conn2.cursor()
    c2.execute("INSERT OR IGNORE INTO last_checks VALUES (null,?,?,?,?,?,?,?)",(exchangeName,pair,duration,setTableName,last_check,seq,last_id))
    conn2.commit()
    c2.execute('SELECT * FROM last_checks')
    setTableName = c2.fetchall()
    for row in setTableName :
        print (row)
    conn2.close()
    conn.close()

def fullDataDB(exchangeName,pair):
    setTableName = str(exchangeName + "_" + pair)
    conn = sqlite3.connect('full_database.db')
    c = conn.cursor()
    tableCreationStatement = """CREATE TABLE IF NOT EXISTS """ + setTableName + """(Id INTEGER PRIMARY KEY, uuid TEXT, traded_btc REAL, price REAL, created_at_int INT, side TEXT,UNIQUE(Id,uuid, side) ON CONFLICT REPLACE)"""
    c.execute(tableCreationStatement)
    conn.commit()
    conn.close()
    
def OrderDB(exchangeName,pair):
    setTableName = str(exchangeName + "_" + pair)
    conn = sqlite3.connect('order_database.db')
    c = conn.cursor()
    tableCreationStatement = """CREATE TABLE IF NOT EXISTS """ + setTableName + """(Id INTEGER PRIMARY KEY, uuid TEXT, traded_btc REAL, price REAL, created_at_int INT, side TEXT,UNIQUE(uuid) ON CONFLICT REPLACE)"""
    c.execute(tableCreationStatement)
    conn.commit()
    conn.close()

def full(exchangeName,pair):
    setTableName = str(exchangeName + "_" + pair)
    conn = sqlite3.connect('full_database.db')
    c = conn.cursor()
    ask_price,ask_volume = test.getDepth(direction='asks',pair=pair)
    c.execute("INSERT INTO "+ setTableName + " VALUES (null,?,?,?,?,?)",(pair,float(ask_volume),float(ask_price),seq,'ask' ))
    bid_price,bid_volume = test.getDepth(direction='bids',pair=pair)
    c.execute("INSERT INTO "+ setTableName + " VALUES (null,?,?,?,?,?)",(pair,bid_volume,bid_price,seq,'bid' ))
    conn.commit()
    c.execute('SELECT * FROM '+ setTableName)
    setTableName = c.fetchall()
    for row in setTableName :
        print (row)
    conn.close()
    
def StoreCandle(exchangeName,pair, duration):
    setTableName = str(exchangeName + "_" + pair+ "_" + duration)
    conn = sqlite3.connect('test_database.db')
    c = conn.cursor()
    #get the data
    data = test.getDataCandle(pair, duration)
    #insert to tableCreationStatement
    
    for elm in data :
        value = [elm['Open time'],elm['High'],elm['Low'],elm['Open'],elm['Close'],elm['Volume'],elm['Quote asset volume']]
        c.execute("INSERT OR IGNORE INTO "+ setTableName + " VALUES (null,?,?,?,?,?,?,?)",value)
        conn.commit()
    c.execute('SELECT * FROM '+ setTableName)
    setTableName = c.fetchall()
    for row in setTableName :
        print (row)
    
    conn.close()



def main():
    #create the table
    exchangeName="Binance"
    pair="ETHBTC"
    duration="5m"
    createDB(exchangeName,pair,duration)
    trackUpdateDB()
    fullDataDB(exchangeName,pair)
    #insert tinto table and update 
    StoreCandle(exchangeName,pair,duration)
    full(exchangeName,pair)
    track(exchangeName,pair,duration)
    
    
if __name__ == "__main__":
    #
    #
    #createDB(exchangeName="Binance",pair="ETHBTC",duration="5m")
    #StoreCandle(exchangeName="Binance",pair="ETHBTC",duration="5m")
    main()
    