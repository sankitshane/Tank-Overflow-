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

@app.route('/')
def start():
    return render_template('index.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
