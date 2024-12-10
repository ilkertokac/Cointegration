from io import StringIO
import requests
import indexId
from typing import Literal
import pandas as pd
import yfinance as yf

def import_stock_list(index_code: Literal["XU100","XU050","XU030"]="XU100"):
    id=indexId.index_id[index_code]
    url="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/Temel-Degerler-Ve-Oranlar.aspx?endeks="+id+"#page-1"
    html_text=requests.get(url).text
    html_io=StringIO(html_text)
    stock_table=pd.read_html(html_io)[2]["Kod"]
    for i in range(len(stock_table)):
        stock_table[i] += ".IS"
    hissekod=sorted(stock_table.to_list())
    return hissekod

def import_price(stock_code,start_date,end_date):
    stock_code=stock_code if stock_code.endswith(".IS") else stock_code+".IS"
    data=pd.DataFrame(yf.download(tickers=stock_code,start=start_date,end=end_date)["Adj Close"])
    return data
