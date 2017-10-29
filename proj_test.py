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
    def __init__(self,*args,**kwargs):
        super(TestApiPost,self).__init__(*args,**kwargs)
        self.response = None

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
        print("Demo data insert...")
        response = requests.get('http://localhost:3000/tankover/api/v1.0/posts')
        self.assertEqual(str(response),"<Response [200]>")
        print("Demo data retrived...")
        retrive_id = loads(dumps(response.json()['cursor'][0]["_id"]["$oid"]))
        response = requests.get('http://localhost:3000/tankover/api/v1.0/posts/'+retrive_id)
        self.assertEqual(str(response),"<Response [200]>")
        print("Demo data retrived specific...")
        response = requests.put('http://localhost:3000/tankover/api/v1.0/posts/'+retrive_id
                                ,json={"_id":retrive_id,"title":"Demo title New"}
                                ,auth=('miguel','python'))
        self.assertEqual(str(response),"<Response [200]>")
        print("Demo data updated...")
        response = requests.put('http://localhost:3000/tankover/api/v1.0/posts/'+retrive_id
                                ,json={"_id":retrive_id,"comments":{"text":"New comment"}}
                                ,auth=('miguel','python'))
        self.assertEqual(str(response),"<Response [200]>")
        print("Demo data comment Added...")
        comment_id = loads(dumps(response.json()['cursor']['comments'][0]['comm_id']))
        response = requests.put('http://localhost:3000/tankover/api/v1.0/posts/'+retrive_id
                                ,json={"_id":retrive_id, "comm_id": str(comment_id),"comments":{"text":"New updated comment"}}
                                ,auth=('miguel','python'))
        self.assertEqual(str(response),"<Response [200]>")
        print("Demo data comment Updated...")
        response = requests.delete('http://localhost:3000/tankover/api/v1.0/posts/'+retrive_id
                                    ,json = ({})
                                    ,auth=("miguel","python"))
        self.assertEqual(response.json(), {'result':True})
        print("Demo data Deleted...")

if __name__ == "__main__":
    unittest.main()
