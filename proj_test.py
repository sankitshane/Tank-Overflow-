import unittest
from flask import Flask
import requests
from bson.json_util import dumps,loads

app_test = Flask(__name__)

class TestFlaskApiUsingRequests(unittest.TestCase):
    def test_hello_world(self):
        response = requests.get('http://localhost:3000')
        self.assertEqual(response.json(), {'hello': 'world'})


if __name__ == "__main__":
    unittest.main()
