import requests

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import mysql.connector
from mysql.connector import errorcode
import datetime

#DB Connection Details
config = {
  'host':'0.0.0.0',
  'user':'root',
  'password':'XXXX',
  'database':'telegram_db'
}

symbol = 'BCH'
#Coinmarketcap API Endpoint
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

#Token to query
parameters = {
'symbol':'BCH'
}

#CoinmarketCap API Connection details

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'e6d4d967-1a7d-4a4a-9e52-6c9191b01031',
}

session = Session()
session.headers.update(headers)

try:

  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  

  current_price = data.get('data').get('BCH').get('quote').get('USD').get('price')
  
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)



#### Connecting to DB
### this code was taken from the official MYSQL dev site
### https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html 
try:
	connection = mysql.connector.connect(**config)
	cursor = connection.cursor()
	
	print("Connection Successful")
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:			
		print("user name or password Error")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:	
		print("Database error")
	else:		
		print("err")

# Writing to DB
try:
	cursor.execute(( "INSERT INTO `price` ("
    "`token_name`, `price`, `date`, `time`) VALUES (%s, %s, %s, %s);"),
	(str(symbol), str(current_price), str(datetime.datetime.now().date()), str(datetime.datetime.now().time()) ))
	
	connection.commit()
except Exception as e:
	print('exception: ' + str(e))
	
		
		

