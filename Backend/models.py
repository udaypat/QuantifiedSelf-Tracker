from datetime import datetime

from main import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


class Tracker(db.Model):
    tid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.String(80))
    desc = db.Column(db.String(140))
    t_type = db.Column(db.Integer)
    settings = db.Column(db.String(200))


class Logs(db.Model):
    lid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    tid = db.Column(db.Integer, db.ForeignKey("tracker.tid"))

    def current_time():
        return datetime.now().replace(microsecond=0)

    timestamp = db.Column(db.DateTime, index=True, default=current_time)

    val = db.Column(db.String(20))
    note = db.Column(db.String(140))
