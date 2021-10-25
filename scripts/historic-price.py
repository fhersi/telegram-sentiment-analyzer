from bs4 import BeautifulSoup
import requests
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector
import datetime

def datify(a):
	result = datetime.datetime.strptime(a, '%b %d, %Y')
	return result.strftime('%d/%m/%Y')

payload = pd.read_html('https://coinmarketcap.com/currencies/ripple/historical-data/?start=20130428&end=20190909')

df = pd.DataFrame(payload[0])
df = df.rename(columns={'Date': 'date'})

df['Name']='XRP'

df['Volume'] = df['Volume'].astype(str)
df['Market Cap'] = df['Market Cap'].astype(str)

df['date']= df['date'].apply(lambda x: datify(x))
df['date'] = pd.to_datetime(df['date'])
df['date'] = df['date'].dt.date

engine = create_engine('mysql+mysqlconnector://XXXX')

df.to_sql('historic_price', con=engine, if_exists = 'append')

engine.execute("SELECT * FROM historic_price").fetchall()



