import sys
import sqlite3
import secrets
import requests
import json

class studyFrenchWords:
	def __init__(self):
		self.connectToDB()
		
	def getWord(self):
		numToTest = secrets.randbelow(9)
		if (numToTest <= 7):
			return self.getGreedyWord()
		else:
			return self.getRandomWord()
	
	def connectToDB(self):
		self.conn=sqlite3.connect('C:\\Users\\anonymous\\Desktop\\frenchwordspractice.db')	
		self.conn.text_factory = lambda x: x.decode(errors='ignore')
		self.c = self.conn.cursor()
		sql = "SELECT * FROM FrenchWord ORDER BY ID DESC LIMIT 1"
		self.c.execute(sql)
		
		rows = self.c.fetchall()
		for row in rows:
			self.numberOfWordsInDict = row[0]
			
	def updateDaysAgoFunction(self):
		sql = "SELECT julianday(CURRENT_DATE) - julianday('"+str(self.oldDate)+"')";
		#print(sql)
		self.c.execute(sql)
		rows = self.c.fetchall()
		for row in rows:
			self.daysAgo = row[0]
		#print(self.daysAgo)
		
	def getWordFromSQLResult(self):
		rows = self.c.fetchall()
		word = ""
		for row in rows:
			#print("Row is " + str(row))
			self.ID = row[0]
			word = row[1]
			self.frequency = row[2]
			self.oldKnowledge = row[3]
			self.oldDate = row[4]
		#print(self.oldDate)
		if (word is None or word == ""):
			print("Word not found.. exiting")
			sys.exit()
		self.updateDaysAgoFunction()

		return word
		
	def getGreedyWord(self):
		sql = "SELECT ID, Word,Frequency,Knowledge,RevisedDate from FrenchWord where CURRENT_DATE != RevisedDate AND SKIPCARD = 0 ORDER BY KnowFreq ASC LIMIT 1;"
		self.c.execute(sql)
		return self.getWordFromSQLResult()
		
	def getRandomWord(self):
		IDToGet = secrets.randbelow(self.numberOfWordsInDict)
		while(IDToGet <= 11):
			IDToGet = secrets.randbelow(self.numberOfWordsInDict)
		sql = "SELECT ID, Word,Frequency,Knowledge,RevisedDate FROM FrenchWord where ID = "+str(IDToGet)
		self.c.execute(sql)
		return self.getWordFromSQLResult()
		
	def updateDB(self, score):
		#apply a weight of 20% to the old value before determining the new knowledge value
		if (score == "skip"):
			sql = "Update FrenchWord Set SkipCard = 1 WHERE ID = "+str(self.ID)
		else:
			#Note this needs to be updated to take a decaying weight of the old score and to be combined with the new score
			sql = "Update FrenchWord Set Knowledge = "+str(score)+" where ID = "+str(self.ID)

		self.c.execute(sql)
		self.conn.commit()
		
	def getCollinsDefinition(self, word):
		headers = {"Content-Type": "application/json", "Host": "api.collinsdictionary.com", "accessKey": "APIKEY"}
		myUrl = "https://api.collinsdictionary.com/api/v1/dictionaries/french-english/search/first/?q="+str(word)+"&format=html"
		myContent = requests.get(myUrl, headers=headers)
		json_data = json.loads(myContent.text)
		try:
			jsonStr = json_data["entryContent"]
		except:
			return ""

		firstInd = jsonStr.find('''<div class=\"hom\"''')
		lastInd = jsonStr.find('''<!-- End of DIV entry lang_fr-->''')

		jsonHTML = jsonStr[firstInd:lastInd]
		jsonHTML = jsonHTML.replace(" &nbsp; ","")
		jsonHTML = jsonHTML.replace("; &nbsp; ","")
		return jsonHTML	
		
	def runProgramLogic(self):
		while(True):
			print("Welcome to French Word Review")
			print("")
			print("The word chosen is "+self.getWord())
			input("Type any key to see Collins French-English dictionary definition")
			print(self.getCollinsDefinition(self.getWord()))
			print("")
			score = input("On a score of 1 to 5 with 1 being really bad and 5 being really good, how well do you know the definition of this word?\nYou may also type skip to skip the word\n")
			self.updateDB(score)
			
sfw = studyFrenchWords()
sfw.runProgramLogic()
