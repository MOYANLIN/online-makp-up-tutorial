from flask import render_template,session,request,redirect,url_for
from app import webapp
from boto3.dynamodb.conditions import Key, Attr

import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

#search content according to key word
@webapp.route('/search',methods=["GET","POST"])
def search():
    search_key = ""
    items = []
    title = ""
    videoimage = ""

    if "username" in session and session['username']!="":
        username=session['username']
    else:
        username=None

    table = dynamodb.Table('video')
    search_key = request.form.get('search_content')
    r = table.scan(
        FilterExpression=Attr('title').contains(search_key)
    )
    items = r['Items']

    if items!=[]:
        isfind=True
        title = r['Items'][0]['title']
        videoimage = "https://s3.amazonaws.com/wonderimage/" + title.split('.')[0]+'.jpg'
    else:
        isfind=False
    return render_template("search.html", items=items, search_key=search_key, title = title, username=username, isfind=isfind)


	
