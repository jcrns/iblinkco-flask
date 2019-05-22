# Importing all needed Flask classes
from flask import g, Blueprint, jsonify, request, make_response, session, url_for, redirect, flash

# Firebase connection
from project.social_apis import firebaseConnect

# Tools for for loops
import itertools

api = Blueprint('api', __name__, template_folder='templates')

# FIREBASE AUTHENTICATION
databaseConnect = firebaseConnect()

database = databaseConnect['database']

authe = databaseConnect['authe']

# Tips
def tips(userReturn):
	tips = []
	print('aaaa')
	description = userReturn['twitter']['userData']['description']
	location = userReturn['twitter']['userData']['location']

	# If conditions are true tips will be given to user
	descriptionLen = len(description)
	print(descriptionLen)
	if descriptionLen < 160:
		descriptionLenMessage = "Only " + str(descriptionLen) + "/180 of your characters have been used for your bio. Explain who you are!"
		tips.append(descriptionLenMessage)
	elif "#" not in description:
		descriptionNoHashtagsMessage = "No Hashtags Found. Try adding hashtags to your bio!"
		tips.append(descriptionLenMessage)
	elif location == "":
		locationIsNoneMessage = "No location found! Add your location so people know where you are located"
		tips.append(locationIsNoneMessage)

	return tips

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
		print("Tips\n\n\n\n\n\n\n\n\n")
		print(userReturn)
	except Exception as e:
		print("Signin error below")
		print(e)
		userData['message'] = 'failed'
		return jsonify(userData)

	# print(user)
	userFinal.append(user)
	userFinal.append(returnedTips)

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


# GOOGLE SEARCH

# Search Function
@api.route("/search-form", methods=['GET', 'POST'])
def searchForm():
	print('searching')

	search = request.form['search']
	connect = googleConnect(search)
	print(connect)

	return jsonify(connect)





