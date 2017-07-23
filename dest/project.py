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
    query = {}
    cursor = posts.find_one()
    return render_template('index.html',cursor = cursor)

@app.route('/post', methods=['GET', 'POST'])
def newpost():
    return render_template('post.html', type = "new")

@app.route('/post/<string:post_id>')
def sub_post(post_id):
    return render_template('post.html', type = "view", post_id = post_id)

@app.route('/post/<string:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    return render_template('post.html', type = "edit", post_id = post_id)

@app.route('/post/<string:post_id>/delete', methods=['GET', 'POST'])
def delete_post(post_id):
    return render_template('post.html', type = "delete", post_id = post_id)

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
    return "Blogs page"

@app.route('/newblog', methods=['GET', 'POST'])
def newBlog():
    return "Add a new Blog"

@app.route('/blog/<string:blog_id>')
def sub_blog(blog_id):
    return "Blogs page " + blog_id

@app.route('/blog/<string:blog_id>/edit', methods=['GET', 'POST'])
def edit_blog(blog_id):
    return "Blogs page " + blog_id

@app.route('/blog/<string:blog_id>/delete', methods=['GET', 'POST'])
def delete_blog(blog_id):
    return "Blogs page " + blog_id

##Login Route
@app.route('/login')
def login():
    return "login page"


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=3000)
