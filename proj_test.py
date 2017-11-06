import unittest
from flask import Flask
import requests
from bson.json_util import dumps,loads
from bson.objectid import ObjectId

app_test = Flask(__name__)

def postFunction(self,funtyp,data,dtype):
    if dtype == "":
        response = requests.post('http://localhost:3000/tankover/api/v1.0/'+funtyp
                                    ,json = (data),
                                    auth=("miguel","python"))
    else:
        response = requests.post('http://localhost:3000/tankover/api/v1.0/'+funtyp+"/"+dtype
                                    ,json = (data),
                                    auth=("miguel","python"))
    self.assertEqual(str(response),"<Response [201]>")
    print("Demo "+ funtyp+" "+dtype  +" data insert...")

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

def addPost(self,funtyp,spec):
    response = requests.put('http://localhost:3000/tankover/api/v1.0/'+funtyp+'/'+spec
                            ,json={"_id":spec,"posts":{"link":"object id of post"}}
                            ,auth=('miguel','python'))
    self.assertEqual(str(response),"<Response [200]>")
    print("Demo "+funtyp+" data post Added...")
    return loads(dumps(response.json()['cursor']['posts']['post_id']))

def updatepost(self,funtyp,spec,spec_ans):
    response = requests.put('http://localhost:3000/tankover/api/v1.0/'+funtyp+'/'+spec
                            ,json={"_id":spec, "post_id": str(spec_ans),"posts":{"link":"New updated object id"}}
                            ,auth=('miguel','python'))
    self.assertEqual(str(response),"<Response [200]>")
    print("Demo "+funtyp+" data post Updated...")

def addOpinion(self,funtyp,spec):
    response = requests.put('http://localhost:3000/tankover/api/v1.0/'+funtyp+'/'+spec
                            ,json={"_id":spec,"crowd opinion":{"text":"that what i think about"}}
                            ,auth=('miguel','python'))
    self.assertEqual(str(response),"<Response [200]>")
    print("Demo "+funtyp+" data opinion Added...")
    return loads(dumps(response.json()['cursor']['crowd opinion']['opinion_id']))

def updateOpinion(self,funtyp,spec,spec_op):
    response = requests.put('http://localhost:3000/tankover/api/v1.0/'+funtyp+'/'+spec
                            ,json={"_id":spec, "opinion_id": str(spec_op),"crowd opinion":{"text":"that what i think about updated"}}
                            ,auth=('miguel','python'))
    self.assertEqual(str(response),"<Response [200]>")
    print("Demo "+funtyp+" data opinion Updated...")

def deleteFunction(self,funtyp,spec):
    response = requests.delete('http://localhost:3000/tankover/api/v1.0/'+funtyp+'/'+spec
                                ,json = ({})
                                ,auth=("miguel","python"))
    self.assertEqual(response.json(), {'result':True})
    print("Demo "+funtyp+" data Deleted...")

def deleteFeature(self,funtyp,feature,spec,spec_id):
    response = requests.delete('http://localhost:3000/tankover/api/v1.0/'+funtyp+'/'+spec
                                ,json = {feature:str(spec_id)}
                                ,auth=("miguel","python"))
    self.assertEqual(response.json(), {'result':True})
    print("Demo "+funtyp+" "+feature+" data Deleted...")

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
        postFunction(self,"posts",postdata,"")
        retrive_id = getFunction(self,"posts")
        getSpecFunction(self,"posts",retrive_id)
        updateFunction(self,"posts",retrive_id)
        comment_id = addComments(self,"posts",retrive_id)
        updateComment(self,"posts",retrive_id,comment_id)
        deleteFeature(self,"posts","comm_id",retrive_id,comment_id)
        deleteFunction(self,"posts",retrive_id)
        print("\n")

class TestApiQuestions(unittest.TestCase):
    def test_question_check(self):
        questiondata = {
            "title":"New Question",
            "description": "Demo description of random topic",
            "tags" : "demotag1 demotag2"
        }
        postFunction(self,"questions",questiondata,"")
        retrive_id = getFunction(self,"questions")
        getSpecFunction(self,"questions",retrive_id)
        updateFunction(self,"questions",retrive_id)
        comment_id = addComments(self,"questions",retrive_id)
        updateComment(self,"questions",retrive_id,comment_id)
        answer_id = addAnswer(self,"questions",retrive_id)
        updateAnswer(self,"questions",retrive_id,answer_id)
        deleteFeature(self,"questions","comm_id",retrive_id,comment_id)
        deleteFeature(self,"questions","ans_id",retrive_id,answer_id)
        deleteFunction(self,"questions",retrive_id)
        print("\n")

class TestApiProject(unittest.TestCase):
    def test_project_check(self):
        projectdata = {
            "title": "New Project",
            "description": "Demo description of random topic",
            "fish": "demofish1 demofish2",
            "plant": "demoplant1 demoplant2",
            "system" : ["Medium","canister","YES","ADA Amozonia","Drogon stone","18x18x15","aquascaping tools"]
        }
        postFunction(self,"projects",projectdata,"")
        retrive_id = getFunction(self,"projects")
        getSpecFunction(self,"projects",retrive_id)
        updateFunction(self,"projects",retrive_id)
        comment_id = addComments(self,"projects",retrive_id)
        updateComment(self,"projects",retrive_id,comment_id)
        post_id = addPost(self,"projects",retrive_id)
        updatepost(self,"projects",retrive_id,post_id)
        deleteFeature(self,"projects","comm_id",retrive_id,comment_id)
        deleteFeature(self,"projects","post_id",retrive_id,post_id)
        deleteFunction(self,"projects",retrive_id)
        print("\n")

class TestApiInfo(unittest.TestCase):
    def test_info_check(self):
        disease_data = {
            "title":"Disease Name",
            "description": "Disease description on the page",
            "images": "demoimage1,demoimage2",
            "identify": "identify1,identify2",
            "treatment": "treatment1,treatment2"
        }
        fish_data = {
            "title": "Neon Tetra",
            "description": "nano fish with bright neon blue color",
            "images": "demoimage1,demoimage2",
            "qstat": [10,"Easy","Peaceful","68-78F","KH 4-8","pH 5-7","2'","Omnivore","Malaysia","Characidae"]
        }
        plant_data = {
            "title": "Dwarf Hairgrass",
            "description": "Dwarf Hairgrass is a great plant for beginners and seasoned aquarium keepers alike",
            "images": "demoimage1,demoimage2",
            "qstat": [" Moderate"," Moderate","Foreground","70-83F","KH 4-8","pH 6.5-7.5","Runners","4'","USA","Cyperaceae"]
        }
        postFunction(self,"info",disease_data,"disease")
        postFunction(self,"info",fish_data,"fish")
        postFunction(self,"info",plant_data,"plant")
        retrive_dieases_id = getFunction(self,"info/disease")
        retrive_fish_id = getFunction(self,"info/fish")
        retrive_plant_id = getFunction(self,"info/plant")
        getSpecFunction(self,"info",retrive_dieases_id)
        getSpecFunction(self,"info",retrive_fish_id)
        getSpecFunction(self,"info",retrive_plant_id)
        updateFunction(self,"info",retrive_dieases_id)
        opinion_id = addOpinion(self,"info",retrive_dieases_id)
        updateOpinion(self,"info",retrive_dieases_id,opinion_id)
        deleteFeature(self,"info","opinion_id",retrive_dieases_id,opinion_id)
        deleteFunction(self,"info",retrive_dieases_id)
        deleteFunction(self,"info",retrive_fish_id)
        deleteFunction(self,"info",retrive_plant_id)
        print("\n")

if __name__ == "__main__":
    unittest.main()
