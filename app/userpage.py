from flask import render_template,session,request,redirect,url_for
from app import webapp
from boto3.dynamodb.conditions import Key, Attr

import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
webapp.config['profile_img']="whileyouweresleeping"

@webapp.route('/user',methods=["GET","POST"])
def user():
    username = session['username']
    table = dynamodb.Table('user')
    r = table.query(
        KeyConditionExpression=Key('username').eq(username)
    )
    data = {}
    data['username'] = r['Items'][0]['username']
    userimg = r['Items'][0]['profileimg']
    if userimg == 'null':
        userimg = 'static/image/DefaultPic.jpg'
    else:
        userimg = "https://s3.amazonaws.com/whileyouweresleeping/" + userimg

    data['profileimg'] = userimg

    if request.method=="POST":
        img = request.files['profileimg']
        username = session['username']
        img_name = username + '_' + img.filename
        table = dynamodb.Table('user')
        table.update_item(
        Key={
            'username': username,
        },
        UpdateExpression="set profileimg = :p",
        ExpressionAttributeValues={
            ':p': img_name
        }
        )
    # store img (img name after padding) to s3
    # upload to s3
        s3 = boto3.client('s3')
        s3.upload_fileobj(img, "whileyouweresleeping", img_name)
    # change the image to be public-read
        s3 = boto3.resource('s3')
        bucket = s3.Bucket("whileyouweresleeping")
        object = s3.Object("whileyouweresleeping", img_name)
        object.Acl().put(ACL="public-read")
        bucket.Acl().put(ACL="public-read")
        return redirect('user')

    return render_template("profile.html", username=username,data=data)


@webapp.route('/changepassword',methods=["GET","POST"])

def change_pwd():
	
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    cf_new_password = request.form.get('cf_new_password')

    #search old password with session['password']
    if old_password != session['password']:
        errors = "Please enter a right old password!"
        return render_template("changepwd.html", errors="Password changed!")

    if new_password != cf_new_password:
        errors = "Please enter the same new password!"
        return render_template("changepwd.html", errors="Password changed!")

    table = dynamodb.Table('user')
    table.update_item(
        Key={
            'username': session["username"],
        },
        UpdateExpression="set password = :pd",
        ExpressionAttributeValues={
            ':pd': new_password
        }
    )
    session['password'] = new_password
    return render_template("changepwd.html", errors="Password changed!")

@webapp.route('/collection',methods=["GET","POST"])

def collection():

    username = session['username']
    table = dynamodb.Table('collection')
    r = table.scan(
    		#ProjectionExpression="video_title",
    		FilterExpression = Attr('username').eq(username),
    	)
    items = r['Items']


    return render_template("colletion.html", items=items)

