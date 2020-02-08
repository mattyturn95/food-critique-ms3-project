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

DEBUG_LEVEL = "DEBUG"

# =========
# HOME PAGE - Display home page featured recipes with
# image and introductory text only
# =========


@app.route("/", methods=["GET", "POST"])
def index():
    # this will allow to display 6 recipes per page. function located in
    # utilities.py file
    pagination = 6
    recipes = mydb.dish.find()

    selected_category = "All Recipes"

    if request.args.get("category"):
        selected_category = (
            request.args.get("category").capitalize() + " Recipes"
        )
          if request.args.get("category"):
        recipes = mydb.dish.find({"category": request.args.get("category")})

    recipes, page, next = paginate(
        recipes, pagination, request.args.get("page")
    )
    return render_template(
        "index.html",
        page=page,
        recipes=recipes,
        next=next,
        categories=get_all_categories_from_db(),
        selected_category=selected_category,
        should_show_background_image=True,
    )


# =================================
# CREATEUSER MODAL- function will allow create new account
# ==================================
@app.route("/create_user", methods=["POST"])
def createuser():
    regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"  # noqa: W605
    if not re.search(regex, request.form.get("email")):
        flash("invalid email")
        return redirect(url_for("index"))

    newuser = {
        "username": request.form.get("username"),
        "password": request.form.get("password"),
        "email": request.form.get("email"),
    }
    user = mydb.users.find_one({"username": request.form["username"]})
    if user:
        flash("Username already exists")
    else:

        try:
            users_col.insert_one(newuser)
            flash(
                "Congratulation "
                + request.form.get("username")
                + "! You have created account"
            )
        # try and except to notify user in case there was some troubleshooting
