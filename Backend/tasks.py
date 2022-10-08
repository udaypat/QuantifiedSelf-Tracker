import sqlalchemy
import pandas as pd
from celery import Celery
from celery.schedules import crontab


import smtplib
from email.message import EmailMessage
from jinja2 import Template


from datetime import date


celery = Celery(broker="redis://localhost:6379")

# For making SQL queries
dbEngine = sqlalchemy.create_engine("sqlite:///database.sqlite3")


@celery.task()
def generate_csv(user):
    query = f"""SELECT lid,timestamp,val,note,logs.tid,name,desc,t_type,settings
    FROM logs
    JOIN tracker ON tracker.tid = logs.tid
    WHERE logs.user_id={user}"""
    df = pd.read_sql(query, dbEngine)
    task_id = celery.current_task.request.id
    file_id = str(task_id)[:8]
    df.to_csv(f"{file_id}_report.csv", index=False)
    return "generation started"


def connect_smtp():
    smtp_server = smtplib.SMTP(host="192.168.0.133", port=1025)
    smtp_server.login("", "")
    return smtp_server


# Setup Email
msg = EmailMessage()
msg["From"] = "csca@c.com"
msg["Subject"] = "hello"


# generates email body
def format_message(username, alert_type, user_id):
    if alert_type == "daily":
        with open("Daily_reminder.html") as ht:
            temp = Template(ht.read())
            message = temp.render(name=username)
        return message

    elif alert_type == "monthly":
        query = f"select * from logs where user_id={user_id}"

        df = pd.read_sql(query, dbEngine)
        user_logs = df.to_dict("records")

        with open("Monthly_report.html") as ht:
            temp = Template(ht.read())
            message = temp.render(logs=user_logs, name=username)
        return message


# Sending email for every recipients
def send_emails(recipients, alert_type):
    smtp_con = connect_smtp()
    for i in recipients:
        msg["To"] = i["email"]

        message = format_message(i["username"], alert_type, i["user_id"])

        msg.add_alternative(message, subtype="html")
        smtp_con.send_message(msg)
        del msg["To"]
        msg.clear_content()
    smtp_con.quit()


# Checking if user has logged any events daily. This will run daily
@celery.task()
def daily_reminder():
    query = "select * from user"
    df = pd.read_sql(query, dbEngine)
    user_list = df.to_dict("records")

    to = date.today()
    recepients = []
    for user in user_list:

        q = f"select * from logs where date(timestamp) = '{to}' and user_id={user['id']}"
        df = pd.read_sql(q, dbEngine)
        dd = df.to_dict("records")
        if len(dd) == 0:
            recepients.append(
                {
                    "username": user["username"],
                    "email": user["email"],
                    "user_id": user["id"],
                }
            )
    send_emails(recepients, "daily")


@celery.task()
def monthly_report():
    query = "select email,id as user_id,username from user"
    df = pd.read_sql(query, dbEngine)
    recepients = df.to_dict("records")
    send_emails(recepients, "monthly")


celery.conf.beat_schedule = {
    "daily-reminder": {
        "task": "tasks.daily_reminder",
        "schedule": crontab(minute=0, hour=23),  # Every night at 11:00 PM
    },
    "monthly-reminder": {
        "task": "tasks.monthly_report",
        "schedule": crontab(0, 22, day_of_month="28"),  # 28th of every month at 10 PM
    },
}

celery.conf.timezone = "Asia/Kolkata"
