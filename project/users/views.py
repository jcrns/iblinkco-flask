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

        # Sending data to API
        getData = requests.post(url = url, json = data) 

        # Getting returned data
        returnedData = getData.json()
        successMessage = returnedData[0]['message']
        email = returnedData[0]['email']
        firstname = returnedData[0]['firstname']
        lastname = returnedData[0]['lastname']

        # Defining variables equal to json data
        instagramData = returnedData[1]
        twitterData = returnedData[2]

        # Storing returned data
        session['name'] = str(firstname) + " " + str(lastname)
        session['email'] = email
        session['instagramData'] = instagramData
        session['twitterData'] = twitterData


        # Alerting user account was created
        flash(f'Account Created for {form.email.data} !', 'success')

        return redirect(url_for('homepage.home'))

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
        returnedData = getData.json()
        try:
            successMessage = returnedData['userdata']['message']
            print(successMessage)
        except Exception as e:
            flash(f'Login Failed')
            return redirect(url_for('users.login'))

        # Defining User Varibles
        email = returnedData['userdata']['email']
        firstname = returnedData['userdata']['firstname']
        lastname = returnedData['userdata']['lastname']

        # Defining variables equal to json data
        instagramData = returnedData['returnedInfoInstagram']
        twitterData = returnedData['returnedInfoTwitter']

        # Storing returned data
        session['name'] = str(firstname) + " " + str(lastname)
        session['email'] = email
        session['instagramData'] = instagramData
        session['twitterData'] = twitterData 


        # Storing all variables in session
        session['instagramBio'] = instagramData['bio']
        session['instagramUsername'] = instagramData['instagram_username']
        session['instagramNumberOfFollowers'] = instagramData['number_of_followers']
        session['instagramNumberOfFollowing'] = instagramData['number_of_following']
        session['instagramNumberOfPost'] = instagramData['number_of_post']
        session['instagramOnDesktop'] = instagramData['on_desktop']
        session['instagramOnMobile'] = instagramData['on_mobile']
        session['instagramOnWeb'] = instagramData['on_web']
        
        session['twitterBio'] = twitterData['bio']
        session['twitterUsername'] = twitterData['twitter_username']
        session['twitterNumberOfFollowers'] = twitterData['number_of_followers']
        session['twitterNumberOfFollowing'] = twitterData['number_of_following']
        session['twitterNumberOfPost'] = instagramData['number_of_post']
        session['twitterOnDesktop'] = twitterData['on_desktop']
        session['twitterOnMobile'] = twitterData['on_mobile']
        session['twitterOnWeb'] = twitterData['on_web']

        session.permanent = True

        return redirect(url_for('homepage.home'))
    return render_template('users/login.html', title="Login", form=form)

@users.route("/logout")
@login_required 
def logout():
    session.clear()
    flash("You have been logged out")
    return redirect(url_for('homepage.home'))