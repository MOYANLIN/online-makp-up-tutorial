from flask import render_template,session,request,redirect,url_for
from app import webapp
from .function import addtwodimdict

import boto3
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

webapp.config['AWS_ACCESS_KEY_ID']=''
webapp.config['AWS_SECRET_ACCESS_KEY']=''

    
@webapp.route('/makeup', methods=['GET','POST'])
def mainpage():
    client=boto3.client('s3',
                aws_access_key_id=webapp.config['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=webapp.config['AWS_SECRET_ACCESS_KEY']
                 )
    s3=boto3.resource('s3')
    bucket=s3.Bucket('wonderimage')
    response = client.list_objects(Bucket='wonderimage')
    table = dynamodb.Table('video')
    imagename=[]
    data={}
    for each in response['Contents']:   #find the cover image of each video
        imagename.append(each['Key'])
        r = table.query(
            KeyConditionExpression=Key('title').eq(each['Key'].split('.')[0])
        )
        addtwodimdict(data, str(each), 'blogger', r['Items'][0]['blogger'])
        addtwodimdict(data, str(each), 'title', r['Items'][0]['title'])
     


    if "username" in session:    #check whether usename in session
        username=session['username']
    else:
        username=None
    return render_template('mainpage.html', data=data, username=username)

        
        
