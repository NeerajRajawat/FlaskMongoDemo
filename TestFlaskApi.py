from flask_pymongo import PyMongo
import flask
from flask import request
from bson.objectid import ObjectId
from bson.json_util import dumps


# create app object
app=flask.Flask("__name__")


# mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/raysdb")
# db = mongodb_client.db

#or
app.config["MONGO_URI"] = "mongodb://localhost:27017/raystech"
mongodb_client = PyMongo(app)
db = mongodb_client.db

@app.route("/add_one",methods=["POST"])
def add_one():
    rollno=request.json["rollno"]
    name=request.json["name"]
    physics=request.json["physics"]
    chemistry=request.json["chemistry"]
    maths=request.json["maths"]
    db.marksheet.insert_one({'rollno': rollno, 
                             'name': name,
                             "physics":physics,
                             "chemistry":chemistry,
                             "maths":maths})
    return flask.jsonify(message="success")

@app.route("/add_many",methods=["post"])
def add_many():
    db.marksheet.insert_many([
        {'rollno': 2, 'name': "Neha","physics":70,"chemistry":89,"maths":90},
        {'rollno': 3, 'name': "Richa","physics":40,"chemistry":29,"maths":93},
        {'rollno': 4, 'name': "Pawan","physics":50,"chemistry":49,"maths":94},
        {'rollno': 5, 'name': "Raghav","physics":70,"chemistry":69,"maths":20},
        {'rollno': 6, 'name': "Madhav","physics":40,"chemistry":79,"maths":93},
       
        ])
    return flask.jsonify(message="success")

# @app.route('/delete/<id>', methods=['DELETE'])
@app.route('/delete/<id>',methods=["delete"])
def delete_user(id):
    # db.marksheet.delete_one({'_id': ObjectId(id)})
    db.marksheet.delete_one({"rollno":int(id)})
    resp = flask.jsonify('User deleted successfully!')
    resp.status_code = 200
    return resp

@app.route("/deleteAll/<id>",methods=["delete"])
def deleteAll(id):
    db.marksheet.delete_many({"rollno":int(id)})
    return "success"

@app.route("/findAll")
def seachAll():
    res=db.marksheet.find()
    marksheetlist=[]
    for item in res:
        marksheet={
            "rollno":item["rollno"],
            "name":item["name"],
            "physics":item["physics"],
            "chemistry":item["chemistry"],
            "maths":item["maths"]
        }
        marksheetlist.append(marksheet)
    
    return flask.jsonify(marksheetlist)

@app.route("/findone/<id>")
def seachOne(id):
    res=db.marksheet.find({"rollno":int(id)})
    marksheetlist=[]
    for item in res:
        marksheet={
            "rollno":item["rollno"],
            "name":item["name"],
            "physics":item["physics"],
            "chemistry":item["chemistry"],
            "maths":item["maths"]
        }
        marksheetlist.append(marksheet)
    return flask.jsonify(marksheetlist)

@app.route("/update/<rollno>",methods=["POST"])
def update_marksheet(rollno):
    name=request.json["name"]
    physics=request.json["physics"]
    chemistry=request.json["chemistry"]
    maths=request.json["maths"]
    marksheet={
        # "rollno":rollno,
        "name":name,
        "physics":physics,
        "chemistry":chemistry,
        "maths":maths
    }
    db.marksheet.update_many({"rollno":int(rollno)},{"$set":marksheet})
    return "success"
# @app.route("/search")
# def searchAll():
#     res=db.marksheet.find()
#     data=dumps(res)
#     return flask.jsonify(data)

# @app.route("/find/<rollno>")
# def seachOne(rollno):
#     res=db.marksheet.find({"rollno":int(rollno)})
#     data=dumps(res)
#     return flask.jsonify(data)



app.run(debug=True, port=5000)

