from flask import Blueprint, render_template
from . import db
blueprint = Blueprint("main", __name__)

@blueprint.route("/", methods=["GET"])
def home():
    return render_template("home.html")