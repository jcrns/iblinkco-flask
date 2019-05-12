# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, url_for, Blueprint

from project.websites.forms import WebsitesForm

# Defining Blueprint var
websites = Blueprint('websites', __name__, template_folder='templates')

@websites.route("/websites")
def home():
    form = WebsitesForm()
    
    # Checking if form is valid
    if form.validate_on_submit():
        data = { 'name': form.name.data, 'email': form.email.data, 'description': form.description.data }
        print(data)
    return render_template('websites/home.html', form=form)
