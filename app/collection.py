from flask import render_template,session,request,redirect,url_for
from app import webapp
from boto3.dynamodb.conditions import Key, Attr
import uuid
import datetime
import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

#add collection to personal list
@webapp.route('/collection/add/',methods=["GET"])
def videoCollection():
    title = request.args.get("title", "")
    username = request.args.get("username", "")
    table = dynamodb.Table('collection')
    r = table.scan(
        FilterExpression=Attr('video_title').eq(title) & Attr('username').eq(username)
    )
    items = r['Items']
    if len(items) != 0:
        data = dict( ok = 0 )
    if len(items) == 0:
        table1 = dynamodb.Table('collection')
        post_time = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        response = table1.put_item(
            Item={
                'id': str(uuid.uuid4()),
                'username': username,
                'video_title': title,
                'collect_time': post_time,
            })
        data = dict( ok = 1 )
    import json
    return json.dumps(data)
