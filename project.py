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
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

app = Flask(__name__)
connection = pymongo.MongoClient("mongodb://localhost")

##auth
@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

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
@auth.login_required
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

@app.route('/tankover/api/v1.0/posts/<string:post_id>', methods=['PUT'])
@auth.login_required
def update_post(post_id):
    db = connection.posthub
    query = {"title": post_id}
    document = db.post.find_one(query)
    if document == None:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    make_new = {}
    for i in request.json:
        make_new[i] = request.json[i]
    toupdate = {'$set':make_new}
    db.post.update(query,toupdate)
    return sub_post(request.json['title'])

@app.route('/tankover/api/v1.0/posts/<string:post_id>', methods=['DELETE'])
@auth.login_required
def delete_post(post_id):
    db = connection.posthub
    query = {'title':post_id}
    document = db.post.find_one(query)
    if document == None:
        abort(404)
    db.post.remove(query)
    return jsonify({'result':True})


##Question Rout
@app.route('/tankover/api/v1.0/questions', methods=['GET'])
def question():
    db = connection.questionhub
    documents = [doc for doc in db.question.find({})]
    return dumps({'cursor': documents})

@app.route('/tankover/api/v1.0/questions/<string:question_id>', methods=['GET'])
def sub_question(question_id):
    db = connection.questionhub
    query = {"title":question_id}
    documents = db.question.find_one(query)
    if documents == None:
        abort(404)
    return dumps({'cursor': documents})

@app.route('/tankover/api/v1.0/questions', methods=['POST'])
@auth.login_required
def newQuestion():
    if not request.json or not 'title' in request.json:
        abort(400)
    tags = request.json['tags'].split()
    addNew = {
                "title": request.json['title'],
                "description":request.json.get('description',''),
                "tags": tags,
                "answer": [],
                "comments":[]
            }
    db = connection.questionhub
    db.question.insert(addNew)
    return dumps({'question':addNew}),201

@app.route('/tankover/api/v1.0/questions/<string:question_id>', methods=['PUT'])
@auth.login_required
def edit_question(question_id):
    db = connection.questionhub
    query = {"title": question_id}
    document = db.question.find_one(query)
    if document == None:
        abort(404)
    if not request.json:
        abort(400)
    if request.json['title'] != question_id:
        abort(400)
    make_new = {}
    for i in request.json:
        if i not in document:
            abort(400)
        make_new[i] = request.json[i]
    toupdate = {'$set':make_new}
    db.question.update(query,toupdate)
    return dumps({"question updated to": make_new}),200

@app.route('/tankover/api/v1.0/questions/<string:question_id>', methods=['DELETE'])
@auth.login_required
def delete_question(question_id):
    db = connection.questionhub
    query = {'title':question_id}
    document = db.question.find_one(query)
    if document == None:
        abort(404)
    db.question.remove(query)
    return jsonify({'result':True})

##Blog Route
@app.route('/tankover/api/v1.0/blogs',methods=['GET'])
def blog():
    db = connection.bloghub
    documents = [doc for doc in db.blog.find({})]
    return dumps({'cursor': documents})

@app.route('/tankover/api/v1.0/blogs/<string:blog_id>', methods=['GET'])
def sub_blog(blog_id):
    db = connection.bloghub
    query = {"title":blog_id}
    documents = db.blog.find_one(query)
    if documents == None:
        abort(404)
    return dumps({'cursor': documents})

@app.route('/tankover/api/v1.0/blogs', methods=['POST'])
@auth.login_required
def newBlog():
    if not request.json or not 'title' in request.json:
        abort(400)
    addNew = {
                "title": request.json['title'],
                "description":request.json.get('description',''),
                "tags": request.json['tags']
            }
    db = connection.bloghub
    db.blog.insert(addNew)
    return dumps({'blog':addNew}),201

@app.route('/tankover/api/v1.0/blogs/<string:blog_id>', methods=['PUT'])
@auth.login_required
def edit_blog(blog_id):
    db = connection.bloghub
    query = {"title": blog_id}
    document = db.blog.find_one(query)
    if document == None:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    make_new = {}
    for i in request.json:
        make_new[i] = request.json[i]
    toupdate = {'$set':make_new}
    db.blog.update(query,toupdate)
    return sub_blog(request.json['title'])

@app.route('/tankover/api/v1.0/blogs/<string:blog_id>', methods=['DELETE'])
@auth.login_required
def delete_blog(blog_id):
    db = connection.bloghub
    query = {'title':blog_id}
    document = db.blog.find_one(query)
    if document == None:
        abort(404)
    db.blog.remove(query)
    return jsonify({'result':True})

##Projects Route
@app.route('/tankover/api/v1.0/projects', methods=['GET'])
def project():
    db = connection.projecthub
    documents = [doc for doc in db.project.find({})]
    return dumps({'cursor': documents})

@app.route('/tankover/api/v1.0/projects/<string:proj_id>', methods=['GET'])
def sub_project(proj_id):
    db = connection.projecthub
    query = {"title":proj_id}
    documents = db.project.find_one(query)
    if documents == None:
        abort(404)
    return dumps({'cursor': documents})

@app.route('/tankover/api/v1.0/projects', methods=['POST'])
@auth.login_required
def newproject():
    if not request.json or not 'title' in request.json:
        abort(400)
    addNew = {
                "title": request.json['title'],
                "description":request.json.get('description',''),
                "tags": request.json['tags']
            }
    db = connection.projecthub
    db.project.insert(addNew)
    return dumps({'post':addNew}),201

@app.route('/tankover/api/v1.0/projects/<string:proj_id>', methods=['PUT'])
@auth.login_required
def edit_project(proj_id):
    db = connection.projecthub
    query = {"title": proj_id}
    document = db.project.find_one(query)
    if document == None:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    make_new = {}
    for i in request.json:
        make_new[i] = request.json[i]
    toupdate = {'$set':make_new}
    db.project.update(query,toupdate)
    return sub_project(request.json['title'])

@app.route('/tankover/api/v1.0/projects/<string:proj_id>', methods=['DELETE'])
@auth.login_required
def delete_blog(proj_id):
    db = connection.projecthub
    query = {'title':proj_id}
    document = db.project.find_one(query)
    if document == None:
        abort(404)
    db.project.remove(query)
    return jsonify({'result':True})

##Login Route
@app.route('/login')
def login():
    return "login page"


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=3000)
