# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, url_for, Blueprint

# Importing forms
from project.users.forms import RegistrationForm, LoginForm, ContactUs

# Importing login_required function
from project.decorators import login_required

# Importing the request library for API
import requests

# Defining Blueprint var
users = Blueprint('users', __name__, template_folder='templates')

def creationFormating(returnedData):
    print("Beggining Format")
    # Defining User Varibles
    email = returnedData['account']['email']
    firstname = returnedData['account']['firstname']
    lastname = returnedData['account']['lastname']
    websiteName = returnedData['website']['website-name']
    websiteUrl = returnedData['website']['website-url']

    # Storing returned data
    session['name'] = str(firstname) + " " + str(lastname)
    session['email'] = email
    session['website_name'] = websiteName
    session['website_url'] = websiteUrl


    # Checking for complete setup
    try:
        setup_complete = returnedData['account']['setup_complete']
        session['setup_complete'] = setup_complete
    except Exception as e:
        print("Setup incomplete")
        print(e)

    # Checking for twitter
    try:
        requestedTwitterUserData = ['description', 'friends_count', 'followers_count', 'location', 'name', 'screen_name']
        returnedTwitterUserData = dict()

        # Defining variables equal to json data
        twitterData = returnedData['twitter']

        for i in requestedTwitterUserData:
            userItem = returnedData['twitter']['userData'][i]
            returnedTwitterUserData[i] = userItem
            print(userItem)
        session['userTwitterData'] = returnedTwitterUserData
        # session['twitter'] = twitterData
    except Exception as e:
        print('Twitter not connected')
        print(e)

    # Checking for instagram
    try:
        # Defining variables equal to json data
        instagramData = returnedData['instagram']

        session['instagram'] = instagramData
    except Exception as e:
        print('Instagram not connected')
        print(e)

# Register page url and function
@users.route("/register", methods=['GET', 'POST'])
def register():
    
    # Defining a variable equal to a form
    form = RegistrationForm()

    # Checking if form is valid
    if form.validate_on_submit():

        # Defining variables equal to post request paramaters
        url = "http://localhost:8000/create-user"
        data = { 'firstname': form.firstname.data, 'lastname': form.lastname.data, 'email': form.email.data, 'password': form.password.data }

        try:
            # Sending data to API
            getData = requests.post(url = url, json = data) 

            # Getting returned data
            returnedData = getData.json()
            email = returnedData[0]['email']
            firstname = returnedData[0]['firstname']
            lastname = returnedData[0]['lastname']

            # Storing returned data
            session['name'] = str(firstname) + " " + str(lastname)
            session['email'] = email
            session['instagramData'] = instagramData
            session['twitterData'] = twitterData


            # Alerting user account was created
            flash(f'Account Created for {form.email.data} !', 'success')
            return redirect(url_for('homepage.home'))
        except Exception as e:
            print(e)
            flash(f'Failed to Create Account')

    return render_template('users/register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():

    # Defining a variable equal to a form
    form = LoginForm()

    # Checking if form is valid
    if form.validate_on_submit():

        # Defining variables equal to post request paramaters
        url = "http://127.0.0.1:8000/signin"
        data = { 'email': form.email.data, 'password': form.password.data }

        # Sending data to API
        getData = requests.post(url = url, json = data) 
        print(getData)

        # Getting returned data
        finalizedData = getData.json()
        # print(finalizedData)
        print(finalizedData)
        session['user'] = finalizedData[1]
        session['tips'] = finalizedData[2]
        returnedData = finalizedData[0]
        # print(returnedData)

        # Getting history
        session['history'] = finalizedData[3]

        # Getting followers' data
        session['followersData'] = finalizedData[4]

        # Getting website data
        session['websiteData'] = finalizedData[5]

        try:

            createFormat = creationFormating(returnedData)
            session.permanent = True

            return redirect(url_for('dashboard.home'))

        except Exception as e:
            print("e")
            print(e)
            flash(f'signin failed')

    return render_template('users/login.html', title="Login", form=form)

@users.route("/logout")
@login_required 
def logout():
    session.clear()
    flash("You have been logged out")
    return redirect(url_for('homepage.home'))