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
	print('aaaaa\n\n\n\n')
	print(website)

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
		if link == '/':
			continue
		if '/' in link:
			fullUrl = str(website) + str(link)
			linkList.append(fullUrl)


	returnList.append(headerTags)
	returnList.append(linkList)

	return returnList

def googleSearch(niche, location, start):
	title_list = []
	link_list = []

	# Getting user data to search
	url = "https://www.googleapis.com/customsearch/v1"
	userInput = str(niche) + " company in " + str(location)

	# Connect google
	parameters = {
		"q": userInput,
		"cx": '001120039411021127475:a4iq_yrptao',
		"key": 'AIzaSyCoVGR41c_O-q7Xz21FduFHtmm37azYTjQ',
		"start": start,
		# "siteSearch": "https://instagram.com"
	}
	page = requests.request("GET", url, params=parameters)
	results = json.loads(page.text)
	
	# Getting title and link through for loop
	for item in results['items']:
		link_list.append(item['link'])
		title_list.append(item['title'])

	returnedData = [title_list, link_list]
	return returnedData

