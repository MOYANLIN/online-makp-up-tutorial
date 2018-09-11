from flask import render_template,session,request,redirect,url_for
from app import webapp

import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

#logout implementation
@webapp.route('/logout',methods=['GET'])
def logout():
    session['username'] = ''
    session['password'] = ''
    return redirect(url_for('mainpage'))
