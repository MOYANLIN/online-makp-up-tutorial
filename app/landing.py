from flask import render_template
from app import webapp

@webapp.route('/', methods=['GET','POST'])
def landing():
    return render_template('landing.html')