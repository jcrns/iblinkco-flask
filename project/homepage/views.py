# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, url_for, Blueprint

# Importing forms
from project.homepage.forms import ContactUs

# Defining Blueprint var
homepage = Blueprint('homepage', __name__, template_folder='templates')


@homepage.route("/", methods=['GET', 'POST'])
def home():

    # Defining a variable equal to a form
    form = ContactUs()

    # Checking if form is valid
    if form.validate_on_submit():
        data = { 'name': form.name.data, 'email': form.email.data, 'message': form.message.data }
        
        print(data)

        return redirect(url_for('home'))

    return render_template('homepage/home.html', form=form)