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
from bson.objectid import ObjectId

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
    query = {"_id":ObjectId(post_id)}
    documents = db.post.find_one(query)
    if documents == None:
        abort(404)
    return dumps({'cursor': documents})

@app.route('/tankover/api/v1.0/posts', methods=['POST'])
@auth.login_required
def newpost():
    if not request.json or not 'title' in request.json:
        abort(400)
    tags = request.json['tags'].split()
    img = request.json['img'].split(",")
    addNew = {
                "title": request.json['title'],
                "description":request.json.get('description',''),
                "tags": tags,
                "images":img,
                "likes":0,
                "comments":[]
            }
    db = connection.posthub
    db.post.insert(addNew)
    return dumps({'post':addNew}),201

@app.route('/tankover/api/v1.0/posts/<string:post_id>', methods=['PUT'])
@auth.login_required
def update_post(post_id):
    db = connection.posthub
    query = {"_id": ObjectId(post_id)}
    document = db.post.find_one(query)
    if document == None:
        abort(404)
    if not request.json:
        abort(400)
    if ObjectId(request.json['_id']) != ObjectId(post_id):
        abort(400)
    make_new = {}
    for i in request.json:
        if i == "_id" or i == "comm_id":
            continue
        make_new[i] = request.json[i]
    if 'comments' in make_new:
        if "comm_id" not in request.json:
            make_new['comments']['comm_id'] = ObjectId()
            toupdate = {"$push":make_new}
        else:
            query = {"_id": ObjectId(post_id),"comments":{"$elemMatch":{"comm_id": ObjectId(request.json['comm_id'])}}}
            toupdate = {"$set":{"comments.$.text":make_new['comments']['text']}}
            print(db.post.find_and_modify(query=query,update=toupdate))
            return dumps({"Updated comment":make_new['comments']['text']}),200
    else:
        toupdate = {'$set':make_new}
    db.post.update(query,toupdate)
    return sub_post(request.json['_id'])

@app.route('/tankover/api/v1.0/posts/<string:post_id>', methods=['DELETE'])
@auth.login_required
def delete_post(post_id):
    db = connection.posthub
    query = {'_id':ObjectId(post_id)}
    document = db.post.find_one(query)
    if document == None:
        abort(404)
    if 'comm_id' in request.json:
        toremove = {"$pull":{"comments":{"comm_id": ObjectId(request.json['comm_id'])}}}
        db.post.update(query,toremove)
    else:
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
    query = {"_id":ObjectId(question_id)}
    documents = db.question.find_one(query)
    if documents == None:
        abort(404)
    return dumps({'cursor': documents})

@app.route('/tankover/api/v1.0/questions', methods=['POST'])
@auth.login_required
def newQuestion():
    print(request.json)
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
    query = {"_id": ObjectId(question_id)}
    document = db.question.find_one(query)
    if document == None:
        abort(404)
    if not request.json:
        abort(400)
    if ObjectId(request.json['_id']) != ObjectId(question_id):
        abort(400)
    make_new = {}
    for i in request.json:
        if i == "_id" or i == "ans_id" or i == "comm_id":
            continue
        if i not in document:
            abort(400)
        make_new[i] = request.json[i]
    if 'answer' in make_new:
        if "ans_id" not in request.json:
            if "ans_com_id" not in request.json:
                make_new["answer"]["ans_id"] = ObjectId()
                toupdate = {"$push":make_new}
        else:
            query = {"_id": ObjectId(question_id),"answer":{"$elemMatch":{"ans_id": ObjectId(request.json['ans_id'])}}}
            toupdate = {'$set':{"answer":make_new['answer']}}
            db.question.find_and_modify(query=query,update=toupdate)
            return dumps({"Added":make_new['answer']}),200
    elif 'comments' in make_new:
        if "comm_id" not in request.json:
            make_new['comments']['comm_id'] = ObjectId()
            toupdate = {"$push":make_new}
        else:
            query = {"_id": ObjectId(question_id),"comments":{"$elemMatch":{"comm_id": ObjectId(request.json['comm_id'])}}}
            toupdate = {"$set":{"comments.$.text":make_new['comments']['text']}}
            db.question.find_and_modify(query=query,update=toupdate)
            return dumps({"Updated comment":make_new['comments']['text']}),200
    else:
        toupdate = {'$set':make_new}
    db.question.update(query,toupdate)
    return dumps({"question updated to": make_new}),200

@app.route('/tankover/api/v1.0/questions/<string:question_id>', methods=['DELETE'])
@auth.login_required
def delete_question(question_id):
    db = connection.questionhub
    query = {'_id':ObjectId(question_id)}
    document = db.question.find_one(query)
    if document == None:
        abort(404)
    if 'ans_id' in request.json:
        toremove = {"$pull":{"answer":{"ans_id":ObjectId(request.json['ans_id'])}}}
        db.question.update(query,toremove)
    if 'comm_id' in request.json:
        toremove = {"$pull":{"comments":{"comm_id":ObjectId(request.json['comm_id'])}}}
        db.question.update(query,toremove)
    else:
        db.question.remove(query)
    return jsonify({'result':True})

##info Route
@app.route('/tankover/api/v1.0/info/disease',methods=['GET'])
def info():
    db = connection.infohub
    documents = [doc for doc in db.info.find({"infotab":"disease"})]
    return dumps({'cursor': documents})

@app.route('/tankover/api/v1.0/info/fish',methods=['GET'])
def info():
    db = connection.infohub
    documents = [doc for doc in db.info.find({"infotab":"fish"})]
    return dumps({'cursor': documents})

@app.route('/tankover/api/v1.0/info/plants',methods=['GET'])
def info():
    db = connection.infohub
    documents = [doc for doc in db.info.find({"infotab":"plants"})]
    return dumps({'cursor': documents})

@app.route('/tankover/api/v1.0/info/<string:info_id>', methods=['GET'])
def sub_info(info_id):
    db = connection.infohub
    query = {"_id":ObjectId(info_id)}
    documents = db.info.find_one(query)
    if documents == None:
        abort(404)
    return dumps({'cursor': documents})

@app.route('/tankover/api/v1.0/info/<string:dtype>', methods=['POST'])
@auth.login_required
def newinfo(dtype):
    if not request.json or not 'name' in request.json:
        abort(400)
    img = request.json['images'].strip(",")
    if dtype == "disease":
        ident = request.json['identify'].split(",")
        treat = request.json['treatment'].split(",")
        addNew = {
                "name": request.json['name'],
                "description":request.json.get('description',''),
                "images": img,
                "identification": ident,
                "treatment": treat,
                "crowd opinion": []
            }
    elif dtype == "fish":
        addNew = {
                "name": request.json['name'],
                "overview": request.json.get('description',''),
                "images":img,
                "quick stat":{
                    "Minimun tank size": request.json['qstat'][0],
                    "Care level": request.json['qstat'][1],
                    "Temperament": request.json['qstat'][2],
                    "Water temp": request.json['qstat'][3],
                    "Water hardnest": request.json['qstat'][4],
                    "Water pH": request.json['qstat'][5],
                    "Max size": request.json['qstat'][6],
                    "Diet": request.json['qstat'][7],
                    "Origin": request.json['qstat'][8],
                    "Family": request.json['qstat'][9]
                }
                "crowd opinion": []
        }
    else:
        addNew = {
                "name":request.json['name'],
                "overview": request.json['description'],
                "images":img,
                "quick stat":{
                    "Care level": request.json['qstat'][0],
                    "Lighting": request.json['qstat'][1],
                    "Placement": request.json['qstat'][2],
                    "Water temp": request.json['qstat'][3],
                    "Water hardnest": request.json['qstat'][4],
                    "Water pH": request.json['qstat'][5],
                    "Propagation": request.json['qstat'][6],
                    "Max size": request.json['qstat'][7],
                    "Origin": request.json['qstat'][8],
                    "Family": request.json['qstat'][9]
                }
                "crowd opinion":[]
            }
    db = connection.infohub
    db.info.insert(addNew)
    return dumps({'info':addNew}),201

@app.route('/tankover/api/v1.0/info/<string:info_id>', methods=['PUT'])
@auth.login_required
def edit_info(info_id):
    db = connection.infohub
    query = {"_id": ObjectId(info_id)}
    document = db.info.find_one(query)
    if document == None:
        abort(404)
    if not request.json:
        abort(400)
    if ObjectId(request.json['_id']) != ObjectId(info_id):
        abort(400)
    make_new = {}
    for i in request.json:
        make_new[i] = request.json[i]
    if 'opinion' in make_new:
        if "opinion_id" not in request.json:
            make_new['opinion']['opinion_id'] = ObjectId()
            toupdate = {"$push":make_new}
        else:
            query = {"_id": ObjectId(info_id),"crowd opinion":{"$elemMatch":{"opinion_id": ObjectId(request.json['opinion_id'])}}}
            toupdate = {"$set":{"comments.$.text":make_new['opinion']['text']}}
            db.question.find_and_modify(query=query,update=toupdate)
            return dumps({"Updated opinion":make_new['opinion']['text']}),200
    else:
        toupdate = {'$set':make_new}
    db.info.update(query,toupdate)
    return sub_info(request.json['_id'])

@app.route('/tankover/api/v1.0/infos/<string:info_id>', methods=['DELETE'])
@auth.login_required
def delete_info(info_id):
    db = connection.infohub
    query = {'_id':ObjectId(info_id)}
    document = db.info.find_one(query)
    if document == None:
        abort(404)
    if 'opinion_id' in request.json:
        toremove = {"$pull":{"crowd opinion":{"opinion_id":ObjectId(request.json['opinion_id'])}}}
        db.question.update(query,toremove)
    else:
        db.info.remove(query)
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
def delete_info(proj_id):
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
