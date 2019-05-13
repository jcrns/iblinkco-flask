from flask import g, Blueprint, jsonify, request, make_response, session, url_for, redirect, flash

from project.social_apis import *

import itertools

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
		userInstagramDefault = {"bio" : "0", "instagram_username" : "none", "number_of_followers" : "0", "number_of_following" : "0", "number_of_post" : "0", "on_desktop" : "False", "on_mobile" : "False", "on_web" : "False"}
		# userTwitterDefault = {"bio" : "0", "twitter_username" : "none", "number_of_followers" : "0", "number_of_following" : "0", "number_of_post" : "0", "on_desktop" : "False", "on_mobile" : "False", "on_web" : "False"}
		userAccount = {"firstname" : firstname, "lastname" : lastname, "email" : email}

		# Assigning uid which will be used to create paths in database
		uid = user['localId']

		# Creating branches
		database.child("users").child(uid).child("data").child("instagram").set(userInstagramDefault)
		database.child("users").child(uid).child("data").child("twitter").set(userTwitterDefault)
		database.child("users").child(uid).child("data").child("account").set(userAccount)
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
		returnedInfoInstagram = dict()
		returnedInfoTwitter = dict()
		
		# For loops to gather information for each branch
		for i in instagramItemList:

			# Getting paths from database and assign to variable
			instagramItem = database.child("users").child(uid).child("data").child("instagram").child(i).get().val()
			print(instagramItem)

			returnedInfoInstagram[i] = str(instagramItem)

		for i in twitterItemList:

			# Getting paths from database and assign to variable
			twitterItem = database.child("users").child(uid).child("data").child("twitter").child(i).get().val()
			returnedInfoTwitter[i] = twitterItem

		for i in userItemList:
			userItem = database.child("users").child(uid).child("data").child("account").child(i).get().val()

			userData[i] = userItem
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

# Getting multiple pages of followers using this function
def nextCursorFollowers(screen_name, followers, next_cursor):
	prev_cursor = followers['previous_cursor']
	# Creating List to hold list
	followersScreenNameList = []
	followersNameList = []

	nextCursor = twitter.request('followers/list.json?screen_name=' + screen_name + '&cursor=' + str(next_cursor))
	nextCursor = nextCursor.data
	
	# Creating For Loop to get all user screen names
	for cursorItem in nextCursor['users']:
		followersItemScreenName = cursorItem['screen_name']
		followersItemName = cursorItem['name']
		followersScreenNameList.append(followersItemScreenName)
		followersNameList.append(followersItemName)
	returnedCursor = nextCursor['next_cursor']
	returnedArray = [returnedCursor, followersScreenNameList, followersNameList]

	# print(followingScreenNameList)
	return returnedArray

# Getting multiple pages of following using this function
def nextCursorFollowing(screen_name, following, next_cursor):
	prev_cursor = following['previous_cursor']
	# Creating List to hold list
	followingScreenNameList = []
	followingNameList = []
	# if next_cursor == 0:
	# 	message = 'finished'
	# 	return message	
	nextCursor = twitter.request('friends/list.json?screen_name=' + screen_name + '&cursor=' + str(next_cursor))
	nextCursor = nextCursor.data
	
	# Creating For Loop to get all user screen names
	for cursorItem in nextCursor['users']:
		followingItemScreenName = cursorItem['screen_name']
		followingItemName = cursorItem['name']
		followingScreenNameList.append(followingItemScreenName)
		followingNameList.append(followingItemName)
	returnedCursor = nextCursor['next_cursor']
	returnedArray = [returnedCursor, followingScreenNameList, followingNameList]

	# print(followingScreenNameList)
	return returnedArray


@api.route('/twitter-oauthorized')
def twitterOauthorized():
	print('dfdff')
	resp = twitter.authorized_response()
	print(resp)
	if resp is None:
		print('You denied the request to sign in.')
	else:
		# Creating List to hold data
		NumberOfTweets = []
		tweetText = []
		favoritesNumber = []
		retweets = []
		comments = []

		followersNameList = []
		followersScreenNameList = []


		followingNameList = []
		followingScreenNameList = []

		screen_name = resp['screen_name']
		print(screen_name)
		session['twitter_oauth'] = resp

		# Getting User Time Line
		# timeline = twitter.request('statuses/home_timeline.json?count=200')
		# tweets = timeline.data
		# print('printing timeline\n\n\n\n\n\n\n\n')
		# print(tweets)

		# Getting User Followers
		getFollowers = twitter.request('followers/list.json?count=200')
		followers = getFollowers.data
		print('printing followers\n\n\n\n\n\n\n\n')
		print(followers)
		firstFollowersCursor = followers['next_cursor']
		firstFollowersPrevCursor = followers['previous_cursor']

		followersCursorList = [firstFollowersCursor]

		for followerItem in followers['users']:
			followerItemScreenName = followerItem['screen_name']
			followerItemName = followerItem['name']
			followersScreenNameList.append(followerItemScreenName)
			followersNameList.append(followerItemName)

		for i in itertools.count():
			print(followersCursorList[i])
			returnedList = nextCursorFollowers(screen_name, followers, followersCursorList[i])
			cursor = returnedList[0]
			if cursor == 0:	
				print("done")
				break
			else:
				userScreenNames = returnedList[1]
				userNames = returnedList[2]
				followersScreenNameList.append(userScreenNames)
				followersNameList.append(userNames)
				followersCursorList.append(cursor)
		print('printing followers\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
		print(followersScreenNameList)
		print(followersNameList)
		print(len(followersScreenNameList))

		# # Getting User Following
		# getFollowering = twitter.request('friends/list.json?count=200')
		# following = getFollowering.data
		# print(following)

		# print('printing following\n\n\n\n\n\n\n\n')
		# # print(following)
		# firstFollowingCursor = following['next_cursor']
		# firstPrevCursor = following['previous_cursor']

		# print('printing following22\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
		# # returnedCursor = nextCursorFollowing(screen_name, following, firstCursor)
		# # print(returnedCursor)

		# followingCursorList = [firstFollowingCursor]


		# # Appending following screen names to list
		# for followingItem in following['users']:
		# 	followingItemScreenName = followingItem['screen_name']
		# 	followingItemName = followingItem['name']
		# 	followingScreenNameList.append(followingItemScreenName)
		# 	followingNameList.append(followingItemName)

		# print(followingScreenNameList)

		# for i in itertools.count():
		# 	print(followingCursorList[i])
		# 	returnedList = nextCursorFollowing(screen_name, following, followingCursorList[i])
		# 	cursor = returnedList[0]
		# 	if cursor == 0:	
		# 		print("done")
		# 		break
		# 	else:
		# 		userScreenNames = returnedList[1]
		# 		userNames = returnedList[2]
		# 		followingScreenNameList.append(userScreenNames)
		# 		followingNameList.append(userNames)
		# 		followingCursorList.append(cursor)

		# print(followingScreenNameList)
		# print(followingNameList)

		# print("cursors" + str(len(followingCursorList)))
		# print("following" + str(len(followingScreenNameList)))

		userData = twitter.request('users/show.json?screen_name=' + screen_name)
		userData = userData.data
		print(userData)

		# Updating twitter data in firebase
		
		# Defining user info
		userLikes = {"user_likes" : userData['statuses_count']}
		userFollowers = {"followers_count" : userData['followers_count']}
		userFollowing = {"following_count" : userData['friends_count']}
		userScreenName = {"screen_name" : userData['screen_name']}
		userName = {"name" : userData['name']}
		bio = {"bio" : userData['description']}

		try:
			# Attemptingto sign in to backend
			user = authe.sign_in_with_email_and_password("jaydencummings1000@gmail.com", "cummings10")

			# Assigning uid as a variable which will be used to go through branched in for loop
			uid = user['localId']

			database.child("users").child(uid).child("data").child("twitter").child("userData").set(userData)
			database.child("users").child(uid).child("data").child("twitter").child("followers").set(followers)

		except Exception as e:
			print(e)
			flash(f'Twitter Login Failed')
			return redirect(url_for('dashboard.home'))
			
	return redirect(url_for('dashboard.home', userInfo=userData, followers=followers))

	# Twitter Search Function Terms




