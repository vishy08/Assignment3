from flask import Flask, jsonify, request
import requests, json
from datetime import datetime
import certifi
from pymongo import MongoClient
client = MongoClient("mongodb+srv://sachith:Jun22!unc@cluster0.sph8g3m.mongodb.net/?retryWrites=true&w=majority", tlsCAFile = certifi.where())
db = client["mydb"]

app = Flask(__name__)
@app.route("/heartrate/last", methods=["GET"])
def heartrate():
    myheader = {"Authorization":"Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhSNkIiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBybnV0IHJwcm8gcnNsZSByYWN0IHJsb2MgcnJlcyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkyMjk1NDQ0LCJpYXQiOjE2NjA3NTk0NDR9.bILcGIrPRXPWRrWBZDKRLsZdtTKKqPUpZ4NZZ-U3k5g"}
    myurl = "https://api.fitbit.com/1/user/-/activities/heart/date/today/1d/1min.json"
    resp = requests.get(myurl, headers=myheader).json()
    
    value = resp["activities-heart-intraday"]["dataset"][-1]["value"]
    
    current = datetime.now()
    time = datetime.now().strftime('%m/%d/%y') + " " + resp["activities-heart-intraday"]["dataset"][-1]["time"]
    change = datetime.strptime(time, '%m/%d/%y %H:%M:%S')
    offset = (current - change).total_seconds()/60
    ret = {'heart-rate': value, 'time offset': offset} 
    return jsonify(ret)  

@app.route("/steps/last", methods=["GET"])
def steps():
    myheader = {"Authorization":"Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhSNkIiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBybnV0IHJwcm8gcnNsZSByYWN0IHJsb2MgcnJlcyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkyMjk1NDQ0LCJpYXQiOjE2NjA3NTk0NDR9.bILcGIrPRXPWRrWBZDKRLsZdtTKKqPUpZ4NZZ-U3k5g"}
    myurl = "https://api.fitbit.com/1/user/-/activities/steps/date/2022-09-14/1d.json"
    distUrl = "https://api.fitbit.com/1/user/-/activities/distance/date/2022-09-14/1d.json"
    resp = requests.get(myurl, headers=myheader).json()
    distResp = requests.get(distUrl, headers=myheader).json()
    steps = resp["activities-steps"][0]["value"]
    distance = distResp["activities-distance"][0]["value"]

    current = datetime.now()
    time = datetime.now().strftime('%m/%d/%y') + " " + resp["activities-steps-intraday"]["dataset"][-1]["time"]
    change = datetime.strptime(time, '%m/%d/%y %H:%M:%S')
    offset = (current - change).total_seconds()/60

    #time = resp["activities"]["duration"]
    ret = {'step-count': steps, 'distance': distance, 'time': offset} 
    return jsonify(ret)              

@app.route('/sleep/<date>', methods=["GET"])
def sleep(date):
    myheader = {"Authorization":"Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhSNkIiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBybnV0IHJwcm8gcnNsZSByYWN0IHJsb2MgcnJlcyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkyMjk1NDQ0LCJpYXQiOjE2NjA3NTk0NDR9.bILcGIrPRXPWRrWBZDKRLsZdtTKKqPUpZ4NZZ-U3k5g"}
    myurl = "https://api.fitbit.com/1.2/user/-/sleep/date/2022-09-14.json"
    resp = requests.get(myurl, headers=myheader).json()
    deep = resp["summary"]["stages"]["deep"]
    light = resp["summary"]["stages"]["light"]
    rem = resp["summary"]["stages"]["rem"]
    wake = resp["summary"]["stages"]["wake"]
    ret = {'deep': deep, 'light': light, 'rem': rem, 'wake': wake}
    return jsonify(ret)    

@app.route("/activeness/<date>", methods=["GET"])
def activeness(date):
    myheader = {"Authorization":"Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhSNkIiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBybnV0IHJwcm8gcnNsZSByYWN0IHJsb2MgcnJlcyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkyMjk1NDQ0LCJpYXQiOjE2NjA3NTk0NDR9.bILcGIrPRXPWRrWBZDKRLsZdtTKKqPUpZ4NZZ-U3k5g"}
    myurl = "https://api.fitbit.com/1/user/-/activities/date/2022-09-14.json"
    resp = requests.get(myurl, headers=myheader).json()
    sedMins = resp["summary"]["sedentaryMinutes"]
    veryActive = resp["summary"]["veryActiveMinutes"]
    lightActive = resp["summary"]["lightlyActiveMinutes"]
    ret = {'very-active': veryActive, 'lightly-active': lightActive, 'sedentary': sedMins}
    return jsonify(ret)

@app.route("/sensors/env", methods=["GET"])
def env():
    # findTemp = db.mycollection().sort(env)
    findTemp = db.env.find().sort("timestamp", -1).limit(1)[0]
    del findTemp["_id"]
    return findTemp

@app.route("/sensors/pose", methods=["GET"])
def pose():
    # findPose = db.mycollection().sort(pose)
    findPose = db.pose.find().sort("timestamp", -1).limit(1)[0]
    del findPose["_id"]
    return findPose

@app.route("/post/env", methods=["POST"])
def postEnv():
    x = request.get_json()
    add = db.env.insert_one(x)
    return "complete"

@app.route("/post/pose", methods=["POST"])
def postPose():
    x = request.get_json()
    add = db.pose.insert_one(x)
    return "complete"

if __name__ == '__main__':
    app.run(debug=True) 