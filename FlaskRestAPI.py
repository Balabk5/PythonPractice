
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
from flask_pymongo import PyMongo
from bson import json_util
from flask_cors import CORS
from flask import jsonify, request
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename  
import pandas as pd
from sklearn.preprocessing import LabelEncoder
#from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


#***************************************monogDB client***********************************************************

password = os.environ.get("MONGODB_PWD")
conntection_string = f"mongodb+srv://balabk5:{password}@cluster0.7xjb73e.mongodb.net/?retryWrites=true&w=majority"



client = MongoClient(conntection_string)
dbs = client.list_database_names()
test_db = client.trail
collections = test_db.list_collection_names()
print(collections)


#*exctracting data from mongodb and setting pandas dataframe

   

collection = test_db.dummy
user = collection.find() 
df = pd.DataFrame(list(collection.find()))
del df["_id"]
print(df)

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
    req = request.get_json()
		
    # _json = request.json
    _age = request.json['age']
    _name = request.json['name']
    
    
    if _name and _age and request.method == 'POST':
        inserted_id = collection.insert_one({'age':_age,'name':_name}).inserted_id
        print(inserted_id)
        resp = jsonify("user added succesfully")
        resp.status_code = 200

        return resp
    else:
        return not_found()
    
col_list_from_client_try=[]
@app.route("/selectedcolumn", methods=['POST'])
def selectedcolumn():
    
    collection = test_db.selectedcolumn
    req = request.get_json()
		
    # _json = request.json
    
    col_0 = request.json[0]
    col_1 = request.json[1]
    col_2 = request.json[2]
    col_3 = request.json[3]
    col_list_from_client = [col_0,col_1,col_2,col_3]
    for i in range(3):
        col_list_from_client_try.append(col_list_from_client[i])
    print(col_list_from_client)
    
    
    if col_0 and col_1 and request.method == 'POST':
        inserted_id = collection.insert_one({'column_0':col_0,'column_1':col_1,'column_2':col_2,'column_3':col_3}).inserted_id
        print(inserted_id)
        resp = jsonify("user added succesfully")
        resp.status_code = 200

        return resp
    else:
        return not_found()
print(col_list_from_client_try)
@app.route("/file", methods=['POST'])
def add_file():
    
    collection = test_db.file
    doc_res = request.files['file']
    
    
    collection.insert_one({'file_name':doc_res})
    resp = jsonify("user added succesfully")
    resp.status_code = 200

    return resp
    
    


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