import pyrebase, json, requests
from flask_oauthlib.client import OAuth
import requests as rq
from bs4 import BeautifulSoup

def firebaseConnect():
	# Configuring connection to database
	config = {
	    'apiKey': "AIzaSyB-zW5qNKkTlfLzhbigIZkMWypJ4XMAAvY",
	    'authDomain': "cpanel-8d88a.firebaseapp.com",
	    'databaseURL': "https://cpanel-8d88a.firebaseio.com",
	    'projectId': "cpanel-8d88a",
	    'storageBucket': "cpanel-8d88a.appspot.com",
	    'messagingSenderId': "955905061850"
	  }

	returnData = dict()

	# Defining variable equal to database connection
	firebase = pyrebase.initialize_app(config)

	# Test Variables
	database = firebase.database()

	returnData['database'] = database

	# Defing users with
	authe = firebase.auth()

	returnData['authe'] = authe


	return returnData

def googleConnect(userInput):
	VALUE = dict()
	url = "https://www.googleapis.com/customsearch/v1"
	parameters = {
		"q": userInput,
		"cx":'001120039411021127475:a4iq_yrptao',
		"key":'AIzaSyCoVGR41c_O-q7Xz21FduFHtmm37azYTjQ',
		"start": 1
	}
	page = requests.request("GET", url, params=parameters)

	allItems = []
	results = json.loads(page.text)
	# print(results['items'])

	for resultItem in results['items']:
		allItems.append(resultItem['link'])
		VALUE['allItems'] = allItems
	
	return VALUE

def twitterConnect():
	oauth = OAuth()
	twitter = oauth.remote_app(
		'twitter',
		consumer_key='QAlCACLnh0Zac3NgdgvXai4mo',
		consumer_secret='xU1L8fYe71matyfq2TNa6CpwVKbXTTS7Y60Sg1VJOmj4WBnjpY',
		base_url='https://api.twitter.com/1.1/',
		request_token_url='https://api.twitter.com/oauth/request_token',
		access_token_url='https://api.twitter.com/oauth/access_token',
		authorize_url='https://api.twitter.com/oauth/authorize'
		
	)
	return twitter

def websiteScrapping(website):
	print('aaalll')
	# Making Request
	r = rq.get(str(website))

	# Defining variable soup
	soup = BeautifulSoup(r.text, 'html.parser')

	# Getting header tags
	headerTags = soup.find('title').text

	# Define return list
	returnList = []
	linkList = []
	# Getting hrefs

	hrefs = soup.find_all('a')
	for href in hrefs:
		link = href['href']	
		if '/' in link:
			fullUrl = str(website) + str(link)
			linkList.append(link)

	returnList.append(headerTags)
	returnList.append(linkList)

	return returnList


