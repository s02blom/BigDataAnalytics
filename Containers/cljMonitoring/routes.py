from flask import Blueprint, render_template, g
import time
blueprint = Blueprint("main", __name__)

@blueprint.route("/", methods=["GET"])
def home():
    print("In / route")
    print(g.start_time, flush=True)
    fake_data = {"count": [0, 10, 20, 30, 40], "time": [time.localtime(10), time.localtime(20), time.localtime(30), time.localtime(40), time.localtime(50)]}
    fake_data2 = []#{"count": [0, 10, 20, 30, 40], "time": [time.localtime(10), time.localtime(20), time.localtime(30), time.localtime(40), time.localtime(50)]}
    
    for i in [0, 10, 20, 30, 40]:
        fake_data2.append({"y": i, "x": time.strftime('%H:%M:%S', time.localtime(i))})
    # return """<h2> Hard coded </h2> <p>Here we listen to Pet Shop Boys</p>"""
    # return render_template("home.html", files_lables=fake_data["count"], files_data=[time.strftime('%Y-%m-%dT%H:%M:%SZ', timestamp) for timestamp in fake_data["time"]] )
    return render_template("home.html", files_data=fake_data2)
