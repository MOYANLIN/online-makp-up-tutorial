from flask import render_template,session,request,redirect,url_for
from app import webapp
from boto3.dynamodb.conditions import Key, Attr
import uuid
import datetime 
import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

@webapp.route('/collect/<string:title>',methods=["GET"])
def collect(title):
    table = dynamodb.Table('video')
    if "username" in session and session['username']!="":
        username=session['username']
    else:
        username=None
    temp=title.split('.')[0]
    r = table.query(
        KeyConditionExpression=Key('title').eq(temp)
    )
    data = {}
    data['tag'] = r['Items'][0]['tag']
    data['likes'] = r['Items'][0]['likes']
    data['blogger']=r['Items'][0]['blogger']
    data['list']=r['Items'][0]['list']
    video_name = "https://s3.amazonaws.com/wondervideo/" + title.split('.')[0]+'.mp4'
    data['video_name'] = video_name
    data['title']=temp
    table= dynamodb.Table('comment')
    r = table.scan(
    		FilterExpression = Attr('video_title').eq(temp),
    	)
    items = r['Items']

    table1 = dynamodb.Table('collection')
    post_time='{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    response = table1.put_item(
        Item={
            'id':str(uuid.uuid4()),
            'username':username,
            'video_title':title.split('.')[0],
            'collect_time':post_time,
            }
    )
	
    return render_template("play.html", data=data, items=items, username=username)
    #return redirect(url_for("play", title=title))
