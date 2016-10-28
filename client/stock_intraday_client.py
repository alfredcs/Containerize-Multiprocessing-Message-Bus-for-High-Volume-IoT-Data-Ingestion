import pandas as pd
import sys, requests, json, fileinput, time
from datetime import datetime
from amqp_pub import amqp_pub
from glob import glob
import pika

proxies = {
    'http': 'http://sjc1intproxy01.crd.xx.com:8080',
    'https': 'http://sjc1intproxy01.crd.xx.com:8080',
}

def get_symbols(file_name, sectors):
  symbols=[]
  fh=glob(file_name)
  for line in fileinput.input(fh):
    #if line.upper().find(sector.upper()) != -1:
    if any( sector.upper() in line.upper() for sector in sectors):
      symbols.append(line.split(",")[1].strip().replace("\"",""))
  return symbols

def get_intraday_data(symbol):
    # Specify URL string based on function inputs.
    keys=['Symbol','Date','Tradetime','Price','Change','Ask','High','Low','Open','Close','Ask','Bid','AskSize','BidSize','AfterHourChange','Volume']
    url_string = 'http://download.finance.yahoo.com/d/quotes.csv?s='+format(symbol.upper())
    url_string += '&f=sd1t1l1c1a5hgopaba5b6c8v'
    # Request the text, and split by each line
    values = requests.get(url_string,  proxies=proxies).text.split(',').replace("\\n", "")
    return  {k:v for k, v in zip(keys, values)}

if __name__ == "__main__":
    #tickers=['AMZN', 'MSFT', 'GOOG'] if len(sys.argv) < 2 else sys.argv[1].split(',')
    #import pdb;pdb.set_trace()
    sectors=['Technology', 'Capital Goods'] if len(sys.argv) < 2 else  sys.argv[1].split(',')
    files="companylist_*.csv"
    tickers= get_symbols(files, sectors)
    while True:
      bodies=[]
      for ticker in tickers:
        #print json.dumps(get_intraday_data(ticker), ensure_ascii=False)
        bodies.append(json.dumps(get_intraday_data(ticker), ensure_ascii=False))
      if amqp_pub.delay(amqp_host='172.20.12.162', bodies=bodies)==False:
        print "Publish failed"
      time.sleep(300)
