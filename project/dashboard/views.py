# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, Blueprint, request, jsonify, g, url_for, make_response

# Importing twitter api
from project.social_apis import twitterConnect, firebaseConnect

# Importing Login Required
from project.decorators import login_required

# Importing formating function
from project.users.views import creationFormating

# Importing tips function
from project.api.views import tips, history, followerData, websites

# Importing counter tool
import itertools

# Importing time to 
from datetime import datetime

dashboard = Blueprint('dashboard', __name__, template_folder='templates')

# FIREBASE AUTHENTICATION
databaseConnect = firebaseConnect()

database = databaseConnect['database']

authe = databaseConnect['authe']

@dashboard.route("/dashboard", methods=['GET', 'POST'])
@login_required
def home():
    print('works')
    return render_template('dashboard/home.html')

# Setup and Website Update
@dashboard.route('/setup-update', methods=['GET', 'POST'])
def updateSetupAndWebsite():
	print("updating")
	try:
		twitter_exist = session['userTwitterData']
		
		# Attemptingto sign in to backend
		user = session['user']

		# Assigning uid as a variable which will be used to go through branched in for loop
		uid = user['localId']
		print('ssss')
		setup_completed = { "setup_complete": True }

		# Adding Setup Complete to Database
		database.child("users").child(uid).child("data").child("account").update({ "setup_complete": True })

		session['setup_complete'] = True
	except Exception as e:
		print("twiiter not connected")
		value = "Twitter not connect"
		return jsonify(value)
	try:
		# Defining variables equal to form input
		website_name = request.form['website_name']
		website_url = request.form['website_url']


		if website_name != '' or website_url != '':
			# Defining json equal to input
			addWebsite = { "website-name" : website_name, "website-url": website_url }

			# Putting json in pyrebase
			database.child("users").child(uid).child("data").child("website").set(addWebsite)

			# Getting database value
			databaseData = dict(database.child("users").child(uid).child("data").get().val())


			formatData = creationFormating(databaseData)
			returnedTips = tips(formatData)
			websites = websites(databaseData)
			session['websiteData'] = websites

			value = "success"
			session['tips'] = returnedTips
		else:		
			value="website form incomplete"
	except Exception as e:
		print("No website")
		print(e)


	return jsonify(value)


# TWITTER OAUTH
twitter = twitterConnect()

@twitter.tokengetter
def get_twitter_token():
    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']


@dashboard.before_request
def before_request():
    g.user = None
    if 'twitter_oauth' in session:
        g.user = session['twitter_oauth']


@dashboard.route('/twitter-getdata')
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
@dashboard.route('/sign-in-twitter')
def twitterLogin():
    callback_url = url_for('dashboard.twitterOauthorized', next=request.args.get('next'))

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


@dashboard.route('/twitter-oauthorized')
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
		# print(userData)

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
			user = session['user']

			# Assigning uid as a variable which will be used to go through branched in for loop
			uid = user['localId']

			# Getting current time 
			now = datetime.now()

			date_time = now.strftime("%m-%d-%Y")

			# Saving data to firebase
			database.child("users").child(uid).child("data").child("twitter").child("userData").set(userData)
			database.child("users").child(uid).child("data").child("twitter").child("followers").set(followers)

			# Saving Data as history
			database.child("users").child(uid).child("data").child("twitter").child("history").child("followers").update({ str(date_time) : userFollowers })
			database.child("users").child(uid).child("data").child("twitter").child("history").child("following").update({ str(date_time) : userFollowing })

			# Formating Twitter Data
			databaseData = dict(database.child("users").child(uid).child("data").get().val())
			formatData = creationFormating(databaseData)

			# Getting Tips
			returnedTips = tips(databaseData)
			session['tips'] = returnedTips

			# Getting history
			historyReturned = history(databaseData)
			session['history'] = historyReturned

			# Getting followers' data
			followersData = followerData(databaseData)
			session['followersData'] = followersData

			# Getting website data
			websitesData = websites(databaseData)
			session['websiteData'] = websiteData

		except Exception as e:
			print(e)
			flash(f'Twitter Login Failed')
			return redirect(url_for('dashboard.home'))
			
	return redirect(url_for('dashboard.home'))

	# Twitter Search Function Terms
