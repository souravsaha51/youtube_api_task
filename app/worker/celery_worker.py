from worker.celery_app import celery_app
from googleapiclient.discovery import build
import json
import mysql.connector
import pymysql.cursors
import pymysql
import mysql.connector
from datetime import timedelta, datetime, timezone

import logging

# Youtube API key.
# Make ENV Variable pushed through docker container.
api_key = "AIzaSyAI-ST49GD3voArhrTmIfsRYid5IvG6tgM"

youtube = build("youtube", "v3", developerKey=api_key)


# MySQL db connection.
# Use env variables in prod inject using docker container
db = mysql.connector.connect(host="mysql", user="root", passwd="my_secret_pw", database="yt_api")
mycursor = db.cursor()

# Celery beat initiation for scheduling the task of pinging youtube constantly.
celery_app.conf.beat_schedule = {
        'youtube-beat': {
            'task': 'youtube_dialer',
            'schedule': timedelta(seconds=10)
        },
    }


# A helper function for youtube dialer in order to asist insertions to the mysql db.
def sql_instert_gen(snippet):
    title = snippet["title"]
    description = snippet["description"]
    publishedAt = snippet["publishedAt"]

    # Preparing SQL query to INSERT a record into the database.
    insert_stmt = "INSERT INTO Football (title, description, publishedAT) VALUES (%s, %s, %s)"
    data = (title, description, publishedAt)

    try:
        # Executing the SQL command
        mycursor.execute(insert_stmt, data)
    
        # Commit your changes in the database
        db.commit()
        return json.dumps({
            "response": "Insertion successful",
            "status": True
        })
    except:
        # Rolling back in case of error
        db.rollback()
        return json.dumps({
            "response": "Database rollback: Unable to execute insertion.",
            "status": False
        })

# Celery task named youtube dialer which is triggered using celery beat every 10 seconds.
@celery_app.task(name="youtube_dialer")
def youtube_dialer():
    latest_timestamp_arg = datetime.now(timezone.utc) - timedelta(hours=0, minutes=0, seconds=30)
    print(latest_timestamp_arg)
    temp = latest_timestamp_arg.astimezone()
    time_to_check = temp.isoformat()

    request = youtube.search().list(
        part="snippet",
        maxResults=5,
        q="football",
        publishedAfter=time_to_check
    )

    response = request.execute()

    if len(response["items"]) > 0:
        for i in response["items"]:
            snippet = i["snippet"]
            insert_command = sql_instert_gen(snippet)
        return json.dumps({
            "response": "Added video data on topic football",
            "status": True
        })

    else:
        return json.dumps({
            "response": "No new videos to be inserted to the table",
            "status": True
        })