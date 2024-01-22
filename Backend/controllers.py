from datetime import datetime

import bcrypt
from flask import jsonify, request, send_file
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from main import app, cache, ma
from models import Logs, Tracker, User, db
from tasks import generate_csv

jwt = JWTManager(app)


salt = bcrypt.gensalt()


# Auto generate Schema using models
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class TrackerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tracker


class LogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Logs


@app.post("/login")
def login():
    # Getting user Creds
    userdata = request.get_json()
    user_name = userdata["username"]
    password = userdata["password"].encode()

    # Getting Creds from db
    curr_user = User.query.filter_by(username=user_name).first()

    # checking creds
    if curr_user is None:
        return jsonify({"msg": "Bad username"})
    elif bcrypt.checkpw(password, curr_user.password):
        # Creating JWT token
        cache.clear()
        access_token = create_access_token(identity=curr_user.id)
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "Bad password"})


# Create User
@app.post("/register")
def register():
    # Getting data
    userdata = request.get_json()
    usr = User.query.filter_by(username=userdata["username"]).first()
    em = User.query.filter_by(email=userdata["email"]).first()

    if usr or em:
        return jsonify("User already Exists")
    password = userdata["password"].encode()

    # Hashing Password
    hashed_pass = bcrypt.hashpw(password, salt)

    # commiting Data
    db.session.add(
        User(
            username=userdata["username"], email=userdata["email"], password=hashed_pass
        ),
    )
    db.session.commit()
    return jsonify("Success")


# trackers list by user with latest values
@cache.memoize(3600)
def user_trackerlist(current_userid):
    trackerslist = Tracker.query.filter_by(user_id=current_userid).all()
    # Converts Sql obeject to json object
    tracker_schema = TrackerSchema(many=True)
    output = tracker_schema.dump(trackerslist)
    latest_dict = {}
    for tracker in trackerslist:
        lo = (
            Logs.query.filter_by(tid=tracker.tid)
            .order_by(Logs.timestamp.desc())
            .first()
        )
        if lo is not None:
            latest_dict[lo.tid] = (lo.timestamp, lo.val)
        else:
            latest_dict[tracker.tid] = ("Not Tracked Yet", "No logs")
    latest = []
    latest.append(latest_dict)
    return jsonify(latest=latest, tlist=output)


# Send list of all Trackers with latest values
@app.route("/trackers")
@jwt_required()
def tracker_list():
    current_userid = get_jwt_identity()
    return user_trackerlist(current_userid)


# Logs by tracker id per user
@cache.memoize(timeout=3600)
def user_logs(current_userid, tracker_id):
    logslist = (
        Logs.query.filter_by(user_id=current_userid, tid=tracker_id)
        .order_by(Logs.timestamp.desc())
        .all()
    )

    # Converts Sql obeject to json object
    log_schema = LogSchema(many=True)
    output = log_schema.dump(logslist)
    return jsonify(output)


# Send all logs for a tracker
@app.route("/<int:tracker_id>/logs")
@jwt_required()
def log_list(tracker_id):
    current_userid = get_jwt_identity()
    return user_logs(current_userid, tracker_id)


# Create a Tracker
@app.post("/create_tracker")
@jwt_required()
def create_tracker():
    current_userid = get_jwt_identity()
    tracker_data = request.get_json()
    db.session.add(
        Tracker(
            user_id=current_userid,
            name=tracker_data["name"],
            desc=tracker_data["desc"],
            t_type=int(tracker_data["type"]),
            settings=tracker_data["settings"],
        )
    )
    db.session.commit()
    tid = Tracker.query.filter_by(
        name=tracker_data["name"], user_id=current_userid
    ).first()
    cache.clear()
    return jsonify({"Tracker ID": tid.tid})


# Get a tracker by ID
@app.route("/tracker/<int:tracker_id>")
@jwt_required()
def tracker(tracker_id):
    current_userid = get_jwt_identity()
    tracker = Tracker.query.filter_by(tid=tracker_id, user_id=current_userid).first()
    tracker_schema = TrackerSchema()
    output = tracker_schema.dump(tracker)
    return jsonify(output)


# Create a log
@app.post("/<int:tracker_id>/create_log")
@jwt_required()
def create_log(tracker_id):
    current_userid = get_jwt_identity()
    log_data = request.get_json()

    try:
        log_data["timestamp"] = datetime.strptime(
            log_data["timestamp"], "%Y-%m-%dT%H:%M"
        )

        db.session.add(
            Logs(
                timestamp=log_data["timestamp"],
                user_id=current_userid,
                tid=tracker_id,
                val=log_data["value"],
                note=log_data["note"],
            )
        )

    except ValueError:
        db.session.add(
            Logs(
                user_id=current_userid,
                tid=tracker_id,
                val=log_data["value"],
                note=log_data["note"],
            )
        )

    db.session.commit()
    cache.clear()
    return jsonify("Log successfully added")


# Get a log by ID
@app.route("/log/<int:log_id>")
@jwt_required()
def log(log_id):
    current_userid = get_jwt_identity()
    curr_log = Logs.query.filter_by(lid=log_id, user_id=current_userid).first()
    if curr_log is None:
        return jsonify("No log found")
    else:
        curr_tracker = Tracker.query.get(curr_log.tid)
        # Converts Sql obeject to json object
        log_schema = LogSchema()
        output = log_schema.dump(curr_log)

        return jsonify(log=output, tracker_id=curr_tracker.tid)


# Update Log
@app.put("/update_log/<int:log_id>")
@jwt_required()
def update_log(log_id):
    current_userid = get_jwt_identity()
    curr_log = Logs.query.filter_by(lid=log_id, user_id=current_userid).first()
    if curr_log is None:
        return jsonify("No log found")
    else:
        log_data = request.get_json()
        curr_log.note = log_data["note"]

        # Converting String to Date
        tobj = datetime.strptime(log_data["timestamp"], "%Y-%m-%dT%H:%M:%S")
        curr_log.timestamp = tobj
        curr_log.val = log_data["val"]
        db.session.commit()
        cache.clear()
        return jsonify(log=log_data, msg="Log updated Successfully")


# Update Tracker
@app.put("/update_tracker/<int:tracker_id>")
@jwt_required()
def update_tracker(tracker_id):
    current_userid = get_jwt_identity()
    curr_tracker = Tracker.query.filter_by(
        tid=tracker_id, user_id=current_userid
    ).first()

    if curr_tracker is None:
        return jsonify("No tracker found")
    else:
        tracker_data = request.get_json()
        curr_tracker.desc = tracker_data["desc"]
        curr_tracker.name = tracker_data["name"]
        curr_tracker.settings = tracker_data["settings"]
        curr_tracker.t_type = tracker_data["t_type"]

        db.session.commit()
        cache.clear()
        return jsonify(tracker_data)


# Delete Tracker
@app.delete("/delete_tracker/<int:trackerid>")
@jwt_required()
def delete_tracker(trackerid):
    current_userid = get_jwt_identity()
    Tracker.query.filter_by(tid=trackerid, user_id=current_userid).delete()
    Logs.query.filter_by(tid=trackerid, user_id=current_userid).delete()
    db.session.commit()
    cache.clear()
    return jsonify("Tracker and it's logs deleted successfully")


# Delete Log
@app.delete("/delete_log/<int:l_id>")
@jwt_required()
def delete_log(l_id):
    current_userid = get_jwt_identity()
    Logs.query.filter_by(lid=l_id, user_id=current_userid).delete()
    db.session.commit()
    cache.clear()
    return jsonify("Log deleted successfully")


# Export as csv
@app.route("/generate_export")
@jwt_required()
def generate_export():
    current_userid = get_jwt_identity()
    task_id = generate_csv.delay(current_userid)
    file_id = str(task_id)[:8]
    return jsonify({"file_id": file_id})


@app.route("/export/<string:file_id>")
@jwt_required()
def export(file_id):
    try:
        return send_file(f"{file_id}_report.csv", as_attachment=True)
    except FileNotFoundError:
        return jsonify("File not generated"), 404


@app.route("/hello")
def hello():
    return "Hello from Flask API"
