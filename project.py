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

##demo
@app.route('/')
def demo():
    return dumps({'hello':'world'})

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
    img = request.json['images'].split()
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
            db.post.find_and_modify(query=query,update=toupdate)
            return dumps({"Updated comment":make_new['comments']['text']}),200
    else:
        toupdate = {'$set':make_new}
    db.post.update(query,toupdate)
    return dumps({"cursor": make_new}),200

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
    if not request.json or not 'title' in request.json:
        abort(400)
    tags = request.json['tags'].split()
    addNew = {
                "title": request.json['title'],
                "description":request.json.get('description',''),
                "tags": tags,
                "answers":[],
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
    if 'answers' in make_new:
        if "ans_id" not in request.json:
            if len(make_new['answers']) == 2:
                make_new["answers"]["ans_id"] = ObjectId()
                toupdate = {"$push":make_new}
            else:
                abort(400)
        else:
            query = {"_id": ObjectId(question_id),"answers":{"$elemMatch":{"ans_id": ObjectId(request.json['ans_id'])}}}
            toupdate = {'$set':{"answers.$.text":make_new['answers']['text'],"answers.$.votes":make_new['answers']['votes']}}
            db.question.find_and_modify(query=query,update=toupdate)
            return dumps({"Added":make_new['answers']}),200
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
    return dumps({"cursor": make_new}),200

@app.route('/tankover/api/v1.0/questions/<string:question_id>', methods=['DELETE'])
@auth.login_required
def delete_question(question_id):
    db = connection.questionhub
    query = {'_id':ObjectId(question_id)}
    document = db.question.find_one(query)
    if document == None:
        abort(404)
    if 'ans_id' in request.json:
        toremove = {"$pull":{"answers":{"ans_id":ObjectId(request.json['ans_id'])}}}
        db.question.update(query,toremove)
    elif 'comm_id' in request.json:
        toremove = {"$pull":{"comments":{"comm_id":ObjectId(request.json['comm_id'])}}}
        db.question.update(query,toremove)
    else:
        db.question.remove(query)
    return jsonify({'result':True})

##info Route
@app.route('/tankover/api/v1.0/info/disease',methods=['GET'])
def infod():
    db = connection.infohub
    documents = [doc for doc in db.info.find({"infotab":"disease"})]
    return dumps({'cursor': documents})

@app.route('/tankover/api/v1.0/info/fish',methods=['GET'])
def infof():
    db = connection.infohub
    documents = [doc for doc in db.info.find({"infotab":"fish"})]
    return dumps({'cursor': documents})

@app.route('/tankover/api/v1.0/info/plant',methods=['GET'])
def infop():
    db = connection.infohub
    documents = [doc for doc in db.info.find({"infotab":"plant"})]
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
    if not request.json or not 'title' in request.json:
        abort(400)
    img = request.json['images'].strip(",")
    if dtype == "disease":
        ident = request.json['identify'].split(",")
        treat = request.json['treatment'].split(",")
        addNew = {
                "infotab" : "disease",
                "title": request.json['title'],
                "description":request.json.get('description',''),
                "images": img,
                "identification": ident,
                "treatment": treat,
                "crowd opinion": []
            }
    if dtype == "fish":
        addNew = {
                "infotab": "fish",
                "title": request.json['title'],
                "overview": request.json.get('description',''),
                "images":img,
                "quick stat":{
                    "Minimun tank size": request.json['qstat'][0],
                    "Care level": request.json['qstat'][1],
                    "Temperament": request.json['qstat'][2],
                    "Water temp": request.json['qstat'][3],
                    "Water hardness": request.json['qstat'][4],
                    "Water pH": request.json['qstat'][5],
                    "Max size": request.json['qstat'][6],
                    "Diet": request.json['qstat'][7],
                    "Origin": request.json['qstat'][8],
                    "Family": request.json['qstat'][9]
                },
                "crowd opinion": []
        }
    if dtype == "plant":
        addNew = {
                "infotab": "plant",
                "title":request.json['title'],
                "overview": request.json['description'],
                "images":img,
                "quick stat":{
                    "Care level": request.json['qstat'][0],
                    "Lighting": request.json['qstat'][1],
                    "Placement": request.json['qstat'][2],
                    "Water temp": request.json['qstat'][3],
                    "Water hardness": request.json['qstat'][4],
                    "Water pH": request.json['qstat'][5],
                    "Propagation": request.json['qstat'][6],
                    "Max size": request.json['qstat'][7],
                    "Origin": request.json['qstat'][8],
                    "Family": request.json['qstat'][9]
                },
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
        if i == "_id" or i == "opinion_id":
            continue
        if i not in document:
            abort(400)
        make_new[i] = request.json[i]
    if 'crowd opinion' in make_new:
        if "opinion_id" not in request.json:
            make_new['crowd opinion']['opinion_id'] = ObjectId()
            toupdate = {"$push":make_new}
        else:
            query = {"_id": ObjectId(info_id),"crowd opinion":{"$elemMatch":{"opinion_id": ObjectId(request.json['opinion_id'])}}}
            toupdate = {"$set":{"crowd opinion.$.text":make_new['crowd opinion']['text']}}
            db.info.find_and_modify(query=query,update=toupdate)
            return dumps({"Updated opinion":make_new['crowd opinion']['text']}),200
    else:
        toupdate = {'$set':make_new}
    db.info.update(query,toupdate)
    return dumps({"cursor": make_new}),200

@app.route('/tankover/api/v1.0/info/<string:info_id>', methods=['DELETE'])
@auth.login_required
def delete_info(info_id):
    db = connection.infohub
    query = {'_id':ObjectId(info_id)}
    document = db.info.find_one(query)
    if document == None:
        abort(404)
    if 'opinion_id' in request.json:
        toremove = {"$pull":{"crowd opinion":{"opinion_id":ObjectId(request.json['opinion_id'])}}}
        db.info.update(query,toremove)
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
    query = {"_id": ObjectId(proj_id)}
    documents = db.project.find_one(query)
    if documents == None:
        abort(404)
    return dumps({'cursor': documents})

@app.route('/tankover/api/v1.0/projects', methods=['POST'])
@auth.login_required
def newproject():
    if not request.json or not 'title' in request.json:
        abort(400)
    fish = request.json['fish'].split()
    plant = request.json['plant'].split()
    addNew = {
                "title": request.json['title'],
                "description":request.json.get('description',''),
                "fish": fish,
                "plants": plant,
                "system": {
                "Lighting": request.json['system'][0],
                "Filtration": request.json['system'][1],
                "CO2": request.json['system'][2],
                "Substrate": request.json['system'][3],
                "Hard scape": request.json['system'][4],
                "Tank size": request.json['system'][5],
                "More tools": request.json['system'][6]
                },
                "posts":[],
                "likes":0,
                "comments":[]
            }
    db = connection.projecthub
    db.project.insert(addNew)
    return dumps({'post':addNew}),201

@app.route('/tankover/api/v1.0/projects/<string:proj_id>', methods=['PUT'])
@auth.login_required
def edit_project(proj_id):
    db = connection.projecthub
    query = {"_id": ObjectId(proj_id)}
    document = db.project.find_one(query)
    if document == None:
        abort(404)
    if not request.json:
        abort(400)
    if ObjectId(request.json['_id']) != ObjectId(proj_id):
        abort(400)
    make_new = {}
    for i in request.json:
        if i == "_id" or i == "comm_id" or i == "post_id":
            continue
        if i not in document:
            abort(400)
        make_new[i] = request.json[i]
    if 'comments' in make_new:
        if "comm_id" not in request.json:
            make_new['comments']['comm_id'] = ObjectId()
            toupdate = {"$push":make_new}
        else:
            query = {"_id": ObjectId(proj_id),"comments":{"$elemMatch":{"comm_id": ObjectId(request.json['comm_id'])}}}
            toupdate = {"$set":{"comments.$.text":make_new['comments']['text']}}
            db.project.find_and_modify(query=query,update=toupdate)
            return dumps({"Updated comment":make_new['comments']['text']}),200
    elif 'posts' in make_new:
        if "post_id" not in request.json:
            make_new['posts']['post_id'] = ObjectId()
            toupdate = {"$push":make_new}
        else:
            query = {"_id": ObjectId(proj_id),"posts":{"$elemMatch":{"post_id": ObjectId(request.json['post_id'])}}}
            toupdate = {"$set":{"posts.$.link":make_new['posts']['link']}}
            db.project.find_and_modify(query=query,update=toupdate)
            return dumps({"Updated posts":make_new['posts']['link']}),200
    else:
        toupdate = {'$set':make_new}
    db.project.update(query,toupdate)
    return dumps({"cursor": make_new}),200

@app.route('/tankover/api/v1.0/projects/<string:proj_id>', methods=['DELETE'])
@auth.login_required
def delete_project(proj_id):
    db = connection.projecthub
    query = {'_id':ObjectId(proj_id)}
    document = db.project.find_one(query)
    if document == None:
        abort(404)
    if 'comm_id' in request.json:
        toremove = {"$pull":{"comments":{"comm_id":ObjectId(request.json['comm_id'])}}}
        db.project.update(query,toremove)
    elif 'post_id' in request.json:
        toremove = {"$pull":{"posts":{"post_id":ObjectId(request.json['post_id'])}}}
        db.project.update(query,toremove)
    else:
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
