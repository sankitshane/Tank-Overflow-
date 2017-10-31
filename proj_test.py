import unittest
from flask import Flask
import requests
from bson.json_util import dumps,loads
from bson.objectid import ObjectId

app_test = Flask(__name__)

def postFunction(self,funtyp,data):
    response = requests.post('http://localhost:3000/tankover/api/v1.0/'+funtyp
                                ,json = (data),
                                auth=("miguel","python"))
    self.assertEqual(str(response),"<Response [201]>")
    print("Demo "+ funtyp +" data insert...")

def getFunction(self,funtyp):
    response = requests.get('http://localhost:3000/tankover/api/v1.0/'+funtyp)
    self.assertEqual(str(response),"<Response [200]>")
    print("Demo "+funtyp+" data retrived...")
    return loads(dumps(response.json()['cursor'][0]["_id"]["$oid"]))

def getSpecFunction(self,funtyp,spec):
    response = requests.get('http://localhost:3000/tankover/api/v1.0/'+funtyp+'/'+spec)
    self.assertEqual(str(response),"<Response [200]>")
    print("Demo "+funtyp+" data retrived specific...")

def updateFunction(self,funtyp,spec):
    response = requests.put('http://localhost:3000/tankover/api/v1.0/'+funtyp+'/'+spec
                            ,json={"_id":spec,"title":"Demo title New"}
                            ,auth=('miguel','python'))
    self.assertEqual(str(response),"<Response [200]>")
    print("Demo "+funtyp+" data updated...")

def addComments(self,funtyp,spec):
    response = requests.put('http://localhost:3000/tankover/api/v1.0/'+funtyp+'/'+spec
                            ,json={"_id":spec,"comments":{"text":"New comment"}}
                            ,auth=('miguel','python'))
    self.assertEqual(str(response),"<Response [200]>")
    print("Demo "+funtyp+" data comment Added...")
    return loads(dumps(response.json()['cursor']['comments']['comm_id']))

def updateComment(self,funtyp,spec,spec_com):
    response = requests.put('http://localhost:3000/tankover/api/v1.0/'+funtyp+'/'+spec
                            ,json={"_id":spec, "comm_id": str(spec_com),"comments":{"text":"New updated comment"}}
                            ,auth=('miguel','python'))
    self.assertEqual(str(response),"<Response [200]>")
    print("Demo "+funtyp+" data comment Updated...")

def addAnswer(self,funtyp,spec):
    response = requests.put('http://localhost:3000/tankover/api/v1.0/'+funtyp+'/'+spec
                            ,json={"_id":spec,"answers":{"text":"New Answer","votes":0}}
                            ,auth=('miguel','python'))
    self.assertEqual(str(response),"<Response [200]>")
    print("Demo "+funtyp+" data Answer Added...")
    return loads(dumps(response.json()['cursor']['answers']['ans_id']))

def updateAnswer(self,funtyp,spec,spec_ans):
    response = requests.put('http://localhost:3000/tankover/api/v1.0/'+funtyp+'/'+spec
                            ,json={"_id":spec, "ans_id": str(spec_ans),"answers":{"text":"New updated answer","votes":2}}
                            ,auth=('miguel','python'))
    self.assertEqual(str(response),"<Response [200]>")
    print("Demo "+funtyp+" data Answer Updated...")

def deleteFunction(self,funtyp,spec):
    response = requests.delete('http://localhost:3000/tankover/api/v1.0/'+funtyp+'/'+spec
                                ,json = ({})
                                ,auth=("miguel","python"))
    self.assertEqual(response.json(), {'result':True})
    print("Demo "+funtyp+" data Deleted...")
    print("\n")

class TestFlaskApiUsingRequests(unittest.TestCase):
    def test_hello_world(self):
        response = requests.get('http://localhost:3000')
        self.assertEqual(response.json(), {'hello': 'world'})

class TestApiPost(unittest.TestCase):
    def test_post_check(self):
        postdata = {
            "title":"Demo Title",
            "description": "Demo description of random topic",
            "tags" : "demotag1 demotag2",
            "images": "demoimage1 demoimage2",
        }
        postFunction(self,"posts",postdata)
        retrive_id = getFunction(self,"posts")
        getSpecFunction(self,"posts",retrive_id)
        updateFunction(self,"posts",retrive_id)
        comment_id = addComments(self,"posts",retrive_id)
        updateComment(self,"posts",retrive_id,comment_id)
        deleteFunction(self,"posts",retrive_id)

class TestApiQuestions(unittest.TestCase):
    def test_question_check(self):
        questiondata = {
            "title":"New Question",
            "description": "Demo description of random topic",
            "tags" : "demotag1 demotag2"
        }
        postFunction(self,"questions",questiondata)
        retrive_id = getFunction(self,"questions")
        getSpecFunction(self,"questions",retrive_id)
        updateFunction(self,"questions",retrive_id)
        comment_id = addComments(self,"questions",retrive_id)
        updateComment(self,"questions",retrive_id,comment_id)
        answer_id = addAnswer(self,"questions",retrive_id)
        updateAnswer(self,"questions",retrive_id,answer_id)
        deleteFunction(self,"questions",retrive_id)


if __name__ == "__main__":
    unittest.main()
