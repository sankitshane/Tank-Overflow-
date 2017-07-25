from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import session as login_session
import random
import string
import httplib2
import json
from flask import make_response
import requests
from datetime import datetime
import pymongo
from pymongo import MongoClient

app = Flask(__name__, static_url_path='', static_folder='')

connection = pymongo.MongoClient("mongodb://localhost")

##Feed Routes
@app.route('/')
@app.route('/post')
def post():
    db = connection.posthub
    posts = db.post
    cursor = posts.find()
    return render_template('index.html',cursor = cursor)

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if request.method == "POST":
        addnew = {"title": request.form['title'],"description":request.form['des']}
        db = connection.posthub
        posts = db.post
        posts.insert(addnew)
        return redirect(url_for('post'))
    return render_template('post.html', type = "new")

@app.route('/post/<string:post_id>')
def sub_post(post_id):
    db = connection.posthub
    query = {"title":post_id}
    post = db.post.find_one(query)
    if post != None:
        return render_template('post.html', type = "view", post = post)
    else:
        return "Please enter the correct ID"

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

##Login Route
@app.route('/login')
def login():
    return "login page"


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=3000)
