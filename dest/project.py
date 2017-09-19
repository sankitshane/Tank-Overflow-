from flask import Flask, request, abort, make_response, jsonify
from flask import session as login_session
import random
import string
import httplib2
import json
import requests
from datetime import datetime
import pymongo
from pymongo import MongoClient
from bson.json_util import dumps,loads


app = Flask(__name__)

connection = pymongo.MongoClient("mongodb://localhost")

##Error Handler
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}),404)

##Feed Routes
@app.route('/tankover/api/v1.0/posts', methods=['GET'])
def post():
    db = connection.posthub
    documents = [doc for doc in db.post.find({})]
    return dumps({'cursor': documents})

@app.route('/tankover/api/v1.0/posts/<string:post_id>', methods=['GET'])
def sub_post(post_id):
    db = connection.posthub
    query = {"title":post_id}
    documents = db.post.find_one(query)
    if documents == None:
        abort(404)
    return dumps({'cursor': documents})

@app.route('/tankover/api/v1.0/posts', methods=['POST'])
def newpost():
    if not request.json or not 'title' in request.json:
        abort(400)
    addNew = {
                "title": request.json['title'],
                "description":request.json.get('description',''),
                "tags": request.json['tags']
            }
    db = connection.posthub
    db.post.insert(addNew)
    return dumps({'post':addNew}),201

@app.route('/post/<string:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    db = connection.posthub
    query = {"title": post_id}
    post = db.post.find_one(query)
    print post
    if request.method == 'POST':
        toupdate = {'$set':{'title':request.form['title'],'description': request.form['des']}}
        db.post.update(query,toupdate)
        return redirect(url_for('post'))
    if post != None:
        return render_template('post.html', type = "edit", post = post)
    else:
        return "Please give a correct ID"

@app.route('/post/<string:post_id>/delete', methods=['GET', 'POST'])
def delete_post(post_id):
    db = connection.posthub
    query = {'title':post_id}
    post = db.post.find_one(query)
    if request.method == 'POST':
        if request.form['bool'] == "YES":
            db.post.remove(query)
        return redirect(url_for('post'))
    if post != None:
        return render_template('post.html', type = "delete", post = post)
    else:
        return "Please give a correct ID"
##Question Rout
@app.route('/question')
def question():
    return render_template('question.html')

@app.route('/newquestion', methods=['GET', 'POST'])
def newQuestion():
    return render_template('question.html', type = "new")

@app.route('/question/<string:question_id>')
def sub_question(question_id):
    return render_template('question.html', type = "view", question_id = question_id)

@app.route('/question/<string:question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    return render_template('question.html', type = "edit", question_id = question_id)

@app.route('/question/<string:question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    return render_template('question.html', type = "delete", question_id = question_id)

##Blog Route
@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/newblog', methods=['GET', 'POST'])
def newBlog():
    return render_template('blog.html', type = "new")

@app.route('/blog/<string:blog_id>')
def sub_blog(blog_id):
    return render_template('blog.html', type = "view", blog_id = blog_id)

@app.route('/blog/<string:blog_id>/edit', methods=['GET', 'POST'])
def edit_blog(blog_id):
    return render_template('blog.html', type = "edit", blog_id = blog_id)

@app.route('/blog/<string:blog_id>/delete', methods=['GET', 'POST'])
def delete_blog(blog_id):
    return render_template('blog.html', type = "delete", blog_id = blog_id)

##Projects Route
@app.route('/project')
def blog():
    return render_template('project.html')

@app.route('/newproj', methods=['GET', 'POST'])
def newBlog():
    return render_template('project.html', type = "new")

@app.route('/project/<string:proj_id>')
def sub_blog(blog_id):
    return render_template('project.html', type = "view", proj_id = blog_id)

@app.route('/project/<string:proj_id>/edit', methods=['GET', 'POST'])
def edit_blog(blog_id):
    return render_template('project.html', type = "edit", proj_id = blog_id)

@app.route('/project/<string:proj_id>/delete', methods=['GET', 'POST'])
def delete_blog(blog_id):
    return render_template('project.html', type = "delete", proj_id = blog_id)

##Login Route
@app.route('/login')
def login():
    return "login page"


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=3000)
