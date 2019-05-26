# Importing all needed Flask classes
from flask import Flask, session, redirect, Blueprint, request, jsonify, g, url_for, make_response

# Firebase connection
from project.social_apis import firebaseConnect, websiteScrapping

# Tools for for loops
import itertools

api = Blueprint('api', __name__, template_folder='templates')

# FIREBASE AUTHENTICATION
databaseConnect = firebaseConnect()

database = databaseConnect['database']

authe = databaseConnect['authe']

# Website
def websites(userReturn):
	websiteData = dict()
	try:
		# Saving required variables
		websiteName = userReturn['website']['website-name']
		websiteUrl = userReturn['website']['website-url']

		websiteData['website-name'] = websiteName
		websiteData['website-url'] = websiteUrl
		
		# Trying other variables
		try:
			headerText = userReturn['website']['header-text']
			links = userReturn['website']['links']
			websiteData['header-text'] = headerText
			websiteData['links'] = links
		except Exception as e:
			print(e)
		print('\n\n\n\n\n\n\n\n\n\n\n\n')
		print(websiteData)
		return websiteData
	except Exception as e:
		 print('Getting Website failed')
		 print(e)

# Tips
def tips(userReturn):
	tips = []
	print('aaaa')
	try:
		# Defining variables

		# Twitter variables
		twitterDescription = userReturn['twitter']['userData']['description']
		twitterName = userReturn['twitter']['userData']['name']
		twitterLocation = userReturn['twitter']['userData']['location']

		# Website variables
		websiteName = userReturn['website']['website-name']
		websiteUrl = userReturn['website']['website-url']

		twitterDescriptionLen = len(twitterDescription)

		twitterFollowers = history(userReturn)

		print('\n\n\n\n\n\n\n\n\n\n\n')
		print(twitterFollowers)
		twitterFollowerNumberList = twitterFollowers[1]
		print(twitterFollowerNumberList)

		# Finding out static trend with for loop
		twitterDaysStatic = 0
		for i in itertools.count():
			print(i)
			if i == len(twitterFollowerNumberList):
				break
			if i == 0:
				i += 1
			if twitterFollowerNumberList[-i] == twitterFollowerNumberList[-i + 1]:
				twitterDaysStatic += 1
		print('daysStatic')
		print(twitterDaysStatic)

		# Trying to give other tips
		try:
			pass
			
		except Exception as e:
			print('no unrequired tips')
			print(e)

		# If conditions are true tips will be given to user
		
		# Programming tips
		if twitterDescriptionLen < 160:
			twitterDescriptionLenMessage = "Only " + str(twitterDescriptionLen) + "/180 of your characters have been used for your bio. Explain who you are!"
			tips.append(twitterDescriptionLenMessage)
		if "#" not in twitterDescription:
			twitterDescriptionNoHashtagsMessage = "No Hashtags Found. Try adding hashtags to your bio!"
			tips.append(twitterDescriptionNoHashtagsMessage)
		if twitterLocation == "":
			twitterLocationIsNoneMessage = "No location found! Add your location so people know where you are located"
			tips.append(twitterLocationIsNoneMessage)
		if websiteName in twitterName or twitterName in websiteName:
			pass
		else:
			websiteNameMessage = "Website name and twitter name are not simular. Try to make it simular!"
		if twitterDaysStatic >= 3:
			twitterDaysStaticTip = "Followers on twitter haven't changed in the last " + str(twitterDaysStatic) + " days. Try posting more and engaging with people."
			tips.append(twitterDaysStaticTip)

		return tips

	except Exception as e:
		print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\ntips error')
		print(e)

# Get History
def history(userReturn):
	try:
		followerHistoryVar = userReturn['twitter']['history']['followers']
		dateList = []
		followerList = []
		for i in followerHistoryVar:
			print(i)
			dateList.append(i)

			date = followerHistoryVar[i]

			followerNumber = date['followers_count'] 
			followerList.append(followerNumber)

		data = []
		data.append(dateList)
		data.append(followerList)
		return data
	except Exception as e:
		print('Trouble getting history')
		print(e)

# Getting followers' data
def followerData(userReturn):
	try:
		print('followw\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
		followersLocatonList = []
		followersNameList = []

		# Getting followers info from database
		followers = userReturn['twitter']['followers']['users']

		# counter
		x = 0
		# For loop getting location and name
		for follow in followers:
			x += 1
			followerLocation = follow['location']
			print(followerLocation)
			followersLocatonList.append(followerLocation)

			followerName = follow['name']
			print(followerName)

			followersNameList.append(followerName)

			if x > 9:
				break
		print(followersLocatonList)
		print(followersNameList)
		data = []
		data.append(followersNameList)
		data.append(followersLocatonList)
		print('\n\n\n\n\n\n\n\n\n\n\n\n')
		return data
	except Exception as e:
		print('Trouble getting follower data returned')
		print(e)

# Sign Up Function
@api.route("/create-user", methods=['GET', 'POST'])
def signUp():
	userData = dict()
	userReturn = []
	
	# Getting posted data and putting it in a dictionary
	print(request.get_json)
	userData['firstname'] = request.get_json()['firstname']
	userData['lastname'] = request.get_json()['lastname']
	userData['email'] = request.get_json()['email']
	userData['password'] = request.get_json()['password']

	# Assigning variables to sign in to database
	firstname = request.json['firstname']
	lastname = request.json['lastname']
	email = request.json['email']
	password = request.json['password']

	print(userData)
	try:
		# Attemptingto sign in to backend
		user = authe.create_user_with_email_and_password(email,password)

		# Assigning json data to variable to return to database
		userAccount = {"firstname" : firstname, "lastname" : lastname, "email" : email, "setup_complete" : False}

		# Assigning uid which will be used to create paths in database
		uid = user['localId']

		# Creating branches
		database.child("users").child(uid).child("data").child("account").set(userAccount)
	except Exception as e:
		print("problem with creation")
		print(e)
		userData['message'] = 'failed'
		return jsonify(userData)
	
	# Appending data into list ready to return
	userReturn.append(userData)
	
	print(userReturn)
	userData['message'] = 'success'

	return jsonify(userReturn)

# Signin Function
@api.route("/signin", methods=['GET', 'POST'])
def signIn():
	userData = dict()

	# Creating list ready to return later
	userFinal = []

	# Assigning values to list for for loop to go though
	userItemList = ['firstname', 'lastname']
	
	# Getting posted data and putting it in a dictionary
	userData['email'] = request.json['email']
	userData['password'] = request.json['password']

	# Assigning variables to sign in to database
	email = request.json['email']
	password = request.json['password']

	try:
		# Attemptingto sign in to backend
		user = authe.sign_in_with_email_and_password(email, password)

		# Assigning uid as a variable which will be used to go through branched in for loop
		uid = user['localId']

		# Creating dict to store data from database
		print(user['localId'])
		userReturn = dict(database.child("users").child(uid).child("data").get().val())
		userFinal.append(userReturn)

		# Tips
		print("Tips\n\n\n\n\n\n\n\n\n")
		returnedTips = tips(userReturn)
		print(returnedTips)

		# History
		historyReturned = history(userReturn)

		# Getting followers data
		followersData = followerData(userReturn)

		# Getting website data
		websitesData = websites(userReturn)

	except Exception as e:
		print("Signin error below")
		print(e)
		userData['message'] = 'failed'
		return jsonify(userData)

	# print(user)
	userFinal.append(user)
	userFinal.append(returnedTips)
	userFinal.append(historyReturned)
	userFinal.append(followersData)
	userFinal.append(websitesData)

	# print(userReturn)
	print(userReturn)

	# Returning main data
	return jsonify(userFinal)

# Signout Function
@api.route("/signout", methods=['POST'])
def signOut():
	if 'user' in session:
		session.pop('user', None)
		session.pop('data', None)
		returnValue = 'Signed Out'
	else:
		returnValue = 'No one is logged in'

	return jsonify({ 'message' : returnValue})


# Connect Website
@api.route("/connect-website", methods=['GET','POST'])
def connectWebsite():
	userData = dict()
	userReturn = []
	try:
		# Defining variables
		websiteName = request.form['website_name']
		websiteUrl = request.form['website_url']

		if websiteName is not None and websiteUrl is not None:
			print('aaa')
			websiteScrap = websiteScrapping(websiteUrl)
			print('aaa')
			
			websiteData = { "website-name" : websiteName, "website-url" : websiteUrl, "header-text" : websiteScrap[0], "links" : websiteScrap[1] }
			print('aaa')

			# Putting them into sessions
			session['websiteData'] = websiteData

			# Importing data in firebase
			user = session['user']

			uid = user['localId']

			database.child("users").child(uid).child("data").child("website").set(websiteData)
			value = 'success'
		else:
			value = 'failed'
		return jsonify(value)
	except Exception as e:
		print('Not dashboard\n\n\n\n\n\n\n')
		print(e)
		print("d")

		# API Request
		try:
			print(request.get_json())

			# Getting posted data
			userData['website-name'] = request.get_json()['website-name']
			userData['website-url'] = request.get_json()['website-url']

			# Defining variables
			websiteName = userData['website-name']
			websiteUrl = userData['website-url']
			
			websiteScrap = websiteScrapping(website_url)
			
			addWebsite = { "website-name" : website_name, "website-url" : website_url, "header-text" : websiteScrap[0], "links" : websiteScrap[1] }

			# Importing data in firebase
			database.child("users").child(uid).child("data").child("website").set(websiteData)

			return jsonify(userData)
		except Exception as e:
			 print('opperation failed')
			 print(e)
			 value = 'failed'

			 return jsonify(value)



# GOOGLE SEARCH

# # Search Function
# @api.route("/search-form", methods=['GET', 'POST'])
# def searchForm():
# 	print('searching')

# 	search = request.form['search']
# 	connect = googleConnect(search)
# 	print(connect)

# 	return jsonify(connect)





