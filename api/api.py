from flask import Flask

api = Flask(__name__)

@api.route('/')
def home():
    return { 'page' : 'home' }

api.run(debug = True, host = '0.0.0.0')
