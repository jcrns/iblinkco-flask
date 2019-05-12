from flask import g, Blueprint, jsonify, request, make_response, session, url_for, redirect

from project.social_apis import *

from time import sleep

api = Blueprint('api', __name__, template_folder='templates')

# FIREBASE AUTHENTICATION
databaseConnect = firebaseConnect()

database = databaseConnect['database']

authe = databaseConnect['authe']


# Sign Up Function
@api.route("/create-user", methods=['GET', 'POST'])
def signUp():
	userData = dict()
	userReturn = []
	
	# Getting posted data and putting it in a dictionary
	print(request.get_json)
	userData['email'] = request.get_json()['email']
	userData['password'] = request.get_json()['password']

	# Assigning variables to sign in to database
	email = request.json['email']
	password = request.json['password']

	print(userData)
	try:
		# Attemptingto sign in to backend
		user = authe.create_user_with_email_and_password(email,password)

		# Assigning json data to variable to return to database
		userInstagramDefault = {"bio" : "0", "instagram_username" : "none", "number_of_followers" : "0", "number_of_following" : "0", "number_of_post" : "0", "on_desktop" : "False", "on_mobile" : "False", "on_web" : "False"}
		userTwitterDefault = {"bio" : "0", "twitter_username" : "none", "number_of_followers" : "0", "number_of_following" : "0", "number_of_post" : "0", "on_desktop" : "False", "on_mobile" : "False", "on_web" : "False"}
		
		# Assigning uid which will be used to create paths in database
		uid = user['localId']

		# Creating branches
		database.child("users").child(uid).child("details").child("instagram").set(userInstagramDefault)
		database.child("users").child(uid).child("details").child("twitter").set(userTwitterDefault)
	except Exception as e:
		print(e)
		userData['message'] = 'failed'
		return jsonify(userData)
	
	# Appending data into list ready to return
	userReturn.append(userData)
	userReturn.append(userInstagramDefault)
	userReturn.append(userTwitterDefault)
	
	print(userReturn)
	userData['message'] = 'success'

	return jsonify(userReturn)

# Signin Function
@api.route("/signin", methods=['POST'])
def signIn():
	userData = dict()

	# Creating list ready to return later
	userReturn = []

	# Assigning values to list for for loop to go though
	instagramItemList = ['bio', 'instagram_username', 'number_of_followers', 'number_of_following', 'number_of_post', 'on_desktop', 'on_mobile', 'on_web']
	twitterItemList = ['bio', 'twitter_username', 'number_of_followers', 'number_of_following', 'number_of_post', 'on_desktop', 'on_mobile', 'on_web']
	
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
		returnedInfoInstagram = dict()
		returnedInfoTwitter = dict()
		
		# For loops to gather information for each branch
		for i in instagramItemList:

			# Getting paths from database and assign to variable
			instagramItem = database.child("users").child(uid).child("details").child("instagram").child(i).get().val()
			print(instagramItem)

			returnedInfoInstagram[i] = str(instagramItem)

		for i in twitterItemList:

			# Getting paths from database and assign to variable
			twitterItem = database.child("users").child(uid).child("details").child("twitter").child(i).get().val()
			returnedInfoTwitter[i] = twitterItem

		if returnedInfoInstagram['instagram_username'] != 'none':
			print('method')

			# This is where we run code because the account is not empty
			
		else:
			print('works')

		if returnedInfoTwitter['twitter_username'] != 'none':
			print('method')

			# This is where we run code because the account is not empty

		else:
			print('works again')
	# If signin or gathering data fails will return failed
	except Exception as e:
		print(e)
		userData['message'] = 'failed'
		return jsonify(userData)

	# Saving success as message
	userData['message'] = 'success'

	# Appending data into list ready to return
	# userReturn['mainobj']['userData] = userData
	# userReturn['mainobj']['returnedInfoInstagram'] = returnedInfoInstagram
	# userReturn['mainobj']['returnedInfoTwitter'] = returnedInfoTwitter

	# userReturn.append({'userdata': userData})
	# userReturn.append({'returnedInfoInstagram': returnedInfoInstagram})
	# userReturn.append({'returnedInfoTwitter': returnedInfoTwitter})

	userReturn={
		'userdata': userData,
		'returnedInfoInstagram': returnedInfoInstagram,
		'returnedInfoTwitter': returnedInfoTwitter
	}
	# Saving gathered data in session
	session['user'] = user
	session['data'] = userReturn
	# print(userReturn)
	print(userReturn)
	# Returning main data
	return jsonify(userReturn)

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


# TWITTER OAUTH
twitter = twitterConnect()

@twitter.tokengetter
def get_twitter_token():
    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']


@api.before_request
def before_request():
    g.user = None
    if 'twitter_oauth' in session:
        g.user = session['twitter_oauth']


@api.route('/twitter-getdata')
def index():
	tweets = None
	if g.user is not None:
		resp = twitter.request('statuses/home_timeline.json')
	if resp.status == 200:
		tweets = resp.data
		print(tweets)
	else:
		print('Unable to load tweets from Twitter.')
	return jsonify(tweets)

# Twitter Sign In function
@api.route('/sign-in-twitter')
def twitterLogin():
    callback_url = url_for('api.twitterOauthorized', next=request.args.get('next'))

    # callback_url = "http://localhost:5000/"
    return twitter.authorize(callback=callback_url)

@api.route('/twitter-oauthorized')
def twitterOauthorized():
	print('dfdff')
	resp = twitter.authorized_response()
	print(resp)
	if resp is None:
		print('You denied the request to sign in.')
	else:
		session['twitter_oauth'] = resp

		# Getting User Time Line
		timeline = twitter.request('statuses/home_timeline.json')
		tweets = timeline.data
		print('printing timeline\n\n\n\n')
		print(tweets)

		# Getting User Followers
		getFollowers = twitter.request('followers/list.json')
		followers = getFollowers.data
		print('printing followers\n\n\n\n')
		print(followers)

		# Getting User Following
		getFollowering = twitter.request('friends/list.json')
		following = getFollowering.data
		print('printing following\n\n\n\n')
		print(following)


	return redirect(url_for('dashboard.home'))




