# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, url_for, Blueprint

# Importing forms
from project.homepage.forms import ContactUs

# Firebase connection
from project.social_apis import firebaseConnect

# Defining Blueprint var
homepage = Blueprint('homepage', __name__, template_folder='templates')

# FIREBASE AUTHENTICATION
databaseConnect = firebaseConnect()

database = databaseConnect['database']

authe = databaseConnect['authe']

@homepage.route("/", methods=['GET', 'POST'])
def home():

    # Defining a variable equal to a form
    form = ContactUs()

    # Checking if form is valid
    if form.validate_on_submit():
        data = { 'email': form.email.data, 'message': form.message.data }
        name = form.name.data
        database.child("contact-us").child(name).update(data)
        print(data)

        return redirect(url_for('homepage.home'))

    return render_template('homepage/home.html', form=form)