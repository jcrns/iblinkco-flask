# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, Blueprint, request, jsonify

# Importing Login Required
from project.decorators import login_required

dashboard = Blueprint('dashboard', __name__, template_folder='templates')

@dashboard.route("/dashboard")
@login_required
def home():
    print('works')
    return render_template('dashboard/home.html')