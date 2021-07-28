from telethon import TelegramClient, events, sync
#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import subprocess
import mysql.connector
from mysql.connector import errorcode
import datetime
import pickle

#set working directory where sentistrength is located
os.chdir("")


#Telegram client authentication details
#Enter your own telegram api details
{
api_id = ''
api_hash = ''
session_name = 'XRP'
chat = 'https://t.me/XRPTraders'
}

# DB authentication details
config = {
  'host':'',
  'user':'root',
  'password':'',
  'database':'telegram_db'
}
		
	


class telegramConnect():
	def __init__(self, api_id,api_hash, chat, session_name):
		self.api_id = api_id
		self.api_hash = api_hash
		self.chat = chat
		self.session_name = session_name


#connect to telegram client 
	def auth(self):
		self.client = TelegramClient(self.session_name, api_id, api_hash)
		self.client.start()

#iterate through messages
	def getMessag(self):	
		return self.client.iter_messages(self.chat, reverse =False)

#prepoccessing to remove white spaces and replace with '+' char
def textProcessing(message):
	return "+".join(message.split())

#Running java program (sentistrength)
def runSubprocess(text):
	content = "java -jar SentiStrengthCom.jar sentidata SentiStrength_Data/ text " + text 
	result = str(subprocess.check_output(content, shell = True))
	#return extractSentiment(result)
	return result

#String splicing to extract positive sentiment
def extractPos(result):
	result = result[2:6].split(" ")
	pos = result[0]
	if pos == None:
		return 0
	else:
		return pos
#String splicing to extract NEG sentiment
def extractNeg(result):
	result = result[2:6].split(" ")
	neg = result[1]
	if neg == None:
		return 0
	else:
		return neg

class sqlAssist():
	
	def __init__(self):
		self.connection = None
		self.cursor = None

#connection to DB
### this code was taken from the official MYSQL dev site
### https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html 
	def connect_to(self):
		
		try:
			
			self.connection = mysql.connector.connect(**config)
			self.cursor = self.connection.cursor()
			
			print("Connection Successful")
			return True
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				
				print("user name or password Error")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				
				print("Database error")
			else:
				
				print("err")
			return False

	def do_close(self):
		
		self.cursor.close()
		self.connection.close()

#Defines how records are inserted into sentiment table
	def insert_record(self, message_id, message_date, current_chat, pos, neg):
		try:
			self.cursor.execute(( "INSERT INTO `sentimentt` ("
               "`group_name`, `message_id`, `message_datetime`, `positivity`, `negativity`) VALUES (%s, %s,%s, %s, %s);"),
				(str(current_chat), str(message_id), message_date, str(pos), str(neg)))
			self.connection.commit()
			return True
		except Exception as e:
			print('write error ' + str(e))
			if '2055' in str(e):
				print('connection timeout')
				return self.connect_to()
			return False


def save(latest_date):
#create a text file and write the current board to it
    outfile = open('C:\\Users\\Vidette\\Desktop\\Farah !!DONT TOUCH!!\\latest_date', 'wb')
    pickle.dump(latest_date, outfile)
    outfile.close()

def load():
#open saved file and store board as board and user as user
    infile = open('C:\\Users\\Vidette\\Desktop\\Farah !!DONT TOUCH!!\\latest_date', 'rb')
    result = pickle.load(infile)
    infile.close()
    return result

def main():

#Last scrape date loaded via pickle
	d = load()
	mutex = 0	
	
	sqlBridge = sqlAssist()
	sqlBridge.connect_to()
	
	client = telegramConnect(api_id, api_hash,chat,session_name)
	client.auth()
	try:

		for message in client.getMessag():
			
			if (message.date <= d) == True:
				print("do_nothing")
			#Save Date of of latest message (since we are scraping from newest to oldest, we are storing date of first message(newest))
			elif mutex < 1:
				save(message.date)
				mutex += 1
			#Filtering for only text messages (GIFS and MULTIMEDIA are filtered out)
			if type(message.text) is str:
				try:
					text = textProcessing(message.text)
					results = runSubprocess(text)
					
					sqlBridge.insert_record(message.id, message.date, session_name, extractPos(results), extractNeg(results))
					
				except Exception as e:
					print(message.id, str(e))	
			
	except Exception as e:
		print('Exception : ', str(e))
	
	sqlBridge.do_close()


if __name__ == '__main__':
    main()

