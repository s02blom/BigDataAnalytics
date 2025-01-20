from flask import Blueprint, render_template, g
import time
blueprint = Blueprint("main", __name__)

@blueprint.route("/", methods=["GET"])
def home():
    chart_data = {}    
    for timer in g.timers.values():
        timer_data = {}
        timer_data["chart_title"] = f"Chart for {timer.collection_name}"
        timer_data["y"] = timer.data["count"]
        timer_data["x"] = timer.data["iso_time"]
        chart_data[timer.collection_name] = timer_data

    return render_template("home.html", chart_data=chart_data, zip=zip)