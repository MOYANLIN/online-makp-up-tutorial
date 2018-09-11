from flask import render_template,request,redirect,url_for,session
from app import webapp

import boto3
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

#login implementation
webapp.secret_key='ece1779'
@webapp.route('/login',methods=['GET'])
def login():
    return render_template("login/login.html")

@webapp.route('/login/check',methods=['POST'])
def login_check():
    table = dynamodb.Table('user')

    username = request.form.get('username')
    password = request.form.get('password')

    response=table.query(
            KeyConditionExpression=Key('username').eq(username)
        )

    if len(response['Items']) == 0:
        return render_template("login/login.html",error="Account doesn't exist!")
    elif response['Items'][0]['password'] != password:
        return render_template("login/login.html", error="Password is wrong!")

    session['username'] = username
    session['password'] = password

    return redirect(url_for("mainpage"))
