from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask import request
from bson.json_util import dumps
from bson.objectid import ObjectId

app=Flask(__name__)

app.config["MONGO_URI"]="mongodb://localhost:27017/bhopal_assignment"

mongo=PyMongo(app)

@app.route("/create_todo", methods=["POST"])
def todo_add():
    data=request.json
    name=data["name"]
    email=data["email"]
    password=data["password"]
    status=data["status"]
    
    todo=mongo.db.todos.insert_one({"name":name,"email":email,"password":password, "status":status})
    return jsonify("Todo Created Successfully")


@app.route("/get_todo",methods=["GET"])
def get_todo():
    todo_list=mongo.db.todos.find()
    result=dumps(todo_list)
    return jsonify(result)



@app.route("/delete_todo/<id>", methods=["DELETE"])
def delete_todo(id):
    del_todo=mongo.db.todos.delete_one({"_id":ObjectId(id)})
    return jsonify("Todo deleted successfully")


# This api for get completed todo or Incompeled todo by sending Complete/Incomplete in url

@app.route("/get_complete_incomplete_todo/<status>",methods=["GET"])
def get_complete_incomplete_todo(status):
    
    complete_incomplete_todo=mongo.db.todos.find_one()
    result=dumps(complete_incomplete_todo)
    return jsonify(result)


if __name__=="__main__":
    app.run(debug=True)
