import os
import re

import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from flask_login import LoginManager
from utilities import paginate
from validators import validate_recipe

load_dotenv()

if os.path.exists("env.py"):
    import env

app = Flask(__name__)
# Get secret key
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
login = LoginManager(app)

# Mongo Database for FITNESS POT
myclient = pymongo.MongoClient(os.environ.get("MONGO_CLUSTER"))
mydb = myclient["fitness_pot"]
dish_col = mydb["dish"]
users_col = mydb["users"]
collection_names = mydb.list_collection_names()