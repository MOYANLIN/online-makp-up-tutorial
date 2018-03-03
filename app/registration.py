from flask import render_template,request,redirect,url_for
from app import webapp

import boto3
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

@webapp.route('/registration',methods=['GET'])
def registration():
    return render_template("register/registration.html")

@webapp.route('/registration/process',methods=['POST'])
def registration_submit():
    table = dynamodb.Table('user')
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get("cfpassword")  # confirm password
    
    if password != confirm_password:
        return render_template("register/registration.html",error="Please enter the same password!")

    response = table.put_item(
        Item={
            'username':username,
            'password':password,
            'profileimg':"null"

        }
    )

    return redirect(url_for('login'))
