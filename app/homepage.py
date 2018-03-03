from flask import render_template,session,request,redirect,url_for
from app import webapp

import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


@webapp.route('/homepage',methods=['GET'])
def homepage():
    table = dynamodb.Table('user')
    username = session['username']
    response = table.get_item(
        Key={
            'username': username
        },
       
    )

    data = {}
    if 'Item' in response:
        item = response['Item']
        data.update(item)

    if data['profileimg'] == 'null':
        profile_img = 'static/image/DefaultPic.jpg'
  
    username = data['username']

    session['username'] = username
 

    return render_template("homepage.html",profileimg=profile_img,username=username)

@webapp.route('/logout',methods=['GET'])
def logout():
    session['username'] = ''
    session['password'] = ''
    return redirect(url_for('mainpage'))
