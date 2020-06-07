from flask import Flask
from routes import account_api


api = Flask(__name__)

#To separte routes file from the run file
api.register_blueprint(account_api)


if __name__ =="__main__":
    api.run(debug = True, host = '0.0.0.0')