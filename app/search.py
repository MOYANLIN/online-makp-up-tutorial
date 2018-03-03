from flask import render_template,session,request,redirect,url_for
from app import webapp
from boto3.dynamodb.conditions import Key, Attr

import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

@webapp.route('/search',methods=["GET","POST"])

def search():
    search_key = ""
    items = []
    title = ""
    videoimage = ""

    table = dynamodb.Table('video')
    search_key = request.form.get('search_content')
    #search_key = search_key.capitalize()
    r = table.scan(
        FilterExpression=Attr('title').contains(search_key)
    )
    items = r['Items']

    if items!=[]:
        title = r['Items'][0]['title']
        videoimage = "https://s3.amazonaws.com/wonderimage/" + title.split('.')[0]+'.jpg'
        return render_template("search.html", items=items, search_key=search_key, title = title)

    else:
        return render_template('404.html')

	
