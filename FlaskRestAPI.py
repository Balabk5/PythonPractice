
import collections




from http import client


import pprint

from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
load_dotenv(find_dotenv())
from flask import Flask
import datetime
import json
from bson import json_util
from flask_cors import CORS, cross_origin
from flask import jsonify, request
from bson.objectid import ObjectId

password = os.environ.get("MONGODB_PWD")
conntection_string = f"mongodb+srv://balabk5:{password}@cluster0.7xjb73e.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(conntection_string)
dbs = client.list_database_names()
test_db = client.trail
collections = test_db.list_collection_names()
print(collections)
  

def insert_test_doc():
    collection = test_db.test
    test_document={
        "name":"bala",
        "type": "testing"
    }
    inserted_id = collection.insert_one(test_document).inserted_id
    print(inserted_id)




production = client.production
person_collection = production.person_collection

def creare_document():
    name = ["bala","kumar","ragul","lenin","amudhesh"]
    age =[21,22,23,24,23,24]

    docs= []

    for names, ages in zip(name,age):
        doc = {"name":names,"age":ages}
        docs.append(doc)

    person_collection.insert_many(docs)




printer = pprint.PrettyPrinter()



def find_person():
    person_name = person_collection.find_one({"name":"bala"})    
    printer.pprint(person_name)



def count_people():
    count = person_collection.count_documents(filter={})
    print("num of people", count)



def get_person_by_id(person_id):
    

    _id = ObjectId(person_id)
    person = person_collection.find_one({"_id":_id})
    printer.pprint(person)



x = datetime.datetime.now()

app = Flask(__name__)
cors = CORS(app)

people_list_doc = []

#*****************************************************************REST API Assignment *****************************************************************************
#all User list
@app.route("/user")
def find_all_people():
    collection = test_db.test
    user = collection.find() 
    return json.loads(json_util.dumps(user))

    
    
    # return json.loads(json_util.dumps(people_list_doc))
@app.route("/user/<id>")
def user(id):
    collection = test_db.test
    user = collection.find_one({'_id':ObjectId(id)})
    return json.loads(json_util.dumps(user))


@app.route("/add", methods=['POST'])
def add_user():
    collection = test_db.test
    _json = request.json
    _name = _json['name']
    _age = _json['age']

    if _name and _age and request.method == 'POST':
        inserted_id = collection.insert_one({'name':_name,'age':_age}).inserted_id
        print(inserted_id)
        resp = jsonify("user added succesfully")
        resp.status_code = 200

        return resp
    else:
        return not_found()


@app.route("/delete/<id>", methods=['DELETE'])        
def delete_user(id):
    collection = test_db.test
    collection.delete_one({'_id':ObjectId(id)})
    resp = jsonify("deleted successfully")

    resp.status_code = 200
    return resp




@app.route("/update/<id>", methods=['PUT'])    
def update_user(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _age = _json['age']

    if _name and _age and request.method == 'PUT':
        collection = test_db.test
        collection.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'name':_name, 'age':_age}})
        resp = jsonify("user updated successfully")
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.errorhandler(404)        
def not_found(error=None):
    message={
        'status':404,
        'message':'not found' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 400




if __name__ == "__main__":
    app.run(debug=True)