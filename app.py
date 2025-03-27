from flask import Flask
from backend.models import db
import os

def setup_ServPro():
    app=Flask(__name__,template_folder="templates",static_folder='static')
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///ServPro.sqlite3" 
    db.init_app(app)
    app.app_context().push()

setup_ServPro()

from backend.controllers import *

if __name__ == "__main__":
    app.run(debug=True)