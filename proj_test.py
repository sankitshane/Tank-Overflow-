import unittest
from flask import Flask
import requests
from bson.json_util import dumps,loads
from bson.objectid import ObjectId

app_test = Flask(__name__)

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
        response = requests.post('http://localhost:3000/tankover/api/v1.0/posts'
                                    ,json = (postdata),
                                    auth=("miguel","python"))
        self.assertEqual(str(response),"<Response [201]>")
        print("Demo post data insert...")
        response = requests.get('http://localhost:3000/tankover/api/v1.0/posts')
        self.assertEqual(str(response),"<Response [200]>")
        print("Demo post data retrived...")
        retrive_id = loads(dumps(response.json()['cursor'][0]["_id"]["$oid"]))
        response = requests.get('http://localhost:3000/tankover/api/v1.0/posts/'+retrive_id)
        self.assertEqual(str(response),"<Response [200]>")
        print("Demo post data retrived specific...")
        response = requests.put('http://localhost:3000/tankover/api/v1.0/posts/'+retrive_id
                                ,json={"_id":retrive_id,"title":"Demo title New"}
                                ,auth=('miguel','python'))
        self.assertEqual(str(response),"<Response [200]>")
        print("Demo post data updated...")
        response = requests.put('http://localhost:3000/tankover/api/v1.0/posts/'+retrive_id
                                ,json={"_id":retrive_id,"comments":{"text":"New comment"}}
                                ,auth=('miguel','python'))
        self.assertEqual(str(response),"<Response [200]>")
        print("Demo post data comment Added...")
        comment_id = loads(dumps(response.json()['cursor']['comments'][0]['comm_id']))
        response = requests.put('http://localhost:3000/tankover/api/v1.0/posts/'+retrive_id
                                ,json={"_id":retrive_id, "comm_id": str(comment_id),"comments":{"text":"New updated comment"}}
                                ,auth=('miguel','python'))
        self.assertEqual(str(response),"<Response [200]>")
        print("Demo post data comment Updated...")
        response = requests.delete('http://localhost:3000/tankover/api/v1.0/posts/'+retrive_id
                                    ,json = ({})
                                    ,auth=("miguel","python"))
        self.assertEqual(response.json(), {'result':True})
        print("Demo post data Deleted...")
        print("\n")

class TestApiQuestions(unittest.TestCase):
    def test_question_check(self):
        questiondata = {
            "title":"New Question",
            "description": "Demo description of random topic",
            "tags" : "demotag1 demotag2"
        }
        response = requests.post('http://localhost:3000/tankover/api/v1.0/questions'
                                    ,json = (questiondata),
                                    auth=("miguel","python"))
        self.assertEqual(str(response),"<Response [201]>")
        print("Demo question data insert...")
        response = requests.get('http://localhost:3000/tankover/api/v1.0/questions')
        self.assertEqual(str(response),"<Response [200]>")
        print("Demo question data retrived...")
        retrive_id = loads(dumps(response.json()['cursor'][0]["_id"]["$oid"]))
        response = requests.get('http://localhost:3000/tankover/api/v1.0/questions/'+retrive_id)
        self.assertEqual(str(response),"<Response [200]>")
        print("Demo question data retrived specific...")
        response = requests.put('http://localhost:3000/tankover/api/v1.0/questions/'+retrive_id
                                ,json={"_id":retrive_id,"title":"Demo title New"}
                                ,auth=('miguel','python'))
        self.assertEqual(str(response),"<Response [200]>")
        print("Demo question data updated...")
        response = requests.put('http://localhost:3000/tankover/api/v1.0/questions/'+retrive_id
                                ,json={"_id":retrive_id,"comments":{"text":"New comment"}}
                                ,auth=('miguel','python'))
        self.assertEqual(str(response),"<Response [200]>")
        print("Demo question data comment Added...")
        comment_id = loads(dumps(response.json()['question updated to']['comments']['comm_id']))
        response = requests.put('http://localhost:3000/tankover/api/v1.0/questions/'+retrive_id
                                ,json={"_id":retrive_id, "comm_id": str(comment_id),"comments":{"text":"New updated comment"}}
                                ,auth=('miguel','python'))
        self.assertEqual(str(response),"<Response [200]>")
        print("Demo question data comment Updated...")
        response = requests.put('http://localhost:3000/tankover/api/v1.0/questions/'+retrive_id
                                ,json={"_id":retrive_id,"answers":{"text":"New Answer","votes":0}}
                                ,auth=('miguel','python'))
        self.assertEqual(str(response),"<Response [200]>")
        print("Demo question data Answer Added...")
        answer_id = loads(dumps(response.json()['question updated to']['answers']['ans_id']))
        response = requests.put('http://localhost:3000/tankover/api/v1.0/questions/'+retrive_id
                                ,json={"_id":retrive_id, "ans_id": str(answer_id),"answers":{"text":"New updated answer","votes":2}}
                                ,auth=('miguel','python'))
        self.assertEqual(str(response),"<Response [200]>")
        print("Demo question data Answer Updated...")
        response = requests.delete('http://localhost:3000/tankover/api/v1.0/questions/'+retrive_id
                                    ,json = ({})
                                    ,auth=("miguel","python"))
        self.assertEqual(response.json(), {'result':True})
        print("Demo question data Deleted...")
        print("\n")


if __name__ == "__main__":
    unittest.main()
