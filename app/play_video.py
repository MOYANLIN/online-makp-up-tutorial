from flask import render_template,session,request,redirect,url_for,flash
from app import webapp
from boto3.dynamodb.conditions import Key, Attr
import uuid
import datetime 
import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

#display specific information of selected video
@webapp.route('/play/<string:title>',methods=["GET","POST"])
def play(title):
    
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
    
    if "username" in session and session['username']!="" and request.method=="POST":
        content=request.form['content']
        if content == None or content=="" or 'content' not in request.form:
            flash(u'Error: Invalid Comment!','warning')
            return redirect(url_for("play", title=title))
        username=session['username']
        usertable=dynamodb.Table('user')
        user_response=usertable.query(
				KeyConditionExpression=Key('username').eq(username)
    		)
        profile_img=user_response['Items'][0]['profileimg']
        table = dynamodb.Table('comment')
    	
        post_time='{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        response = table.put_item(
            Item={
                'id':str(uuid.uuid4()),
                'content':content,
                'username':username,
                'video_title':title.split('.')[0],
                'post_time':post_time,
                'profile_img':profile_img,
                }
        )
        return redirect(url_for("play", title=title))
    return render_template("play.html", data=data, items=items, username=username)
