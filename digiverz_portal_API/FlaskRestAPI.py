
import collections
from http import client
from inspect import _void
import pprint
from tokenize import Name
from dotenv import load_dotenv, find_dotenv
import os
import sys
import bson
import pickle
import pprint
import pandas_profiling as pp
import seaborn as sns

from pymongo import MongoClient
load_dotenv(find_dotenv())
from flask import Flask
import datetime
import json
import numpy as np
from flask_pymongo import PyMongo
from bson import json_util
from flask_cors import CORS
from flask import jsonify, request
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename  
import pandas as pd
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import when, lit,regexp_replace,substring,to_timestamp,to_date,col
from pyspark.sql.types import DoubleType,StringType
from sklearn.preprocessing import LabelEncoder
from pyspark.sql.types import *
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
test_db = client.trail
collections = test_db.list_collection_names()
# print(collections)
#*spark session.................................................
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
spark = SparkSession.builder.appName('First_App').getOrCreate()
spark.conf.set('spark.sql.repl.eagerEval.enabled', True)

#*exctracting data from mongodb and setting pandas dataframe

   

import sys

sys.setrecursionlimit(10**6)
print(sys.getrecursionlimit())



# collection=test_db.file
# record = collection.find_one({'_id':ObjectId('6340252034bbeaeb2a18cb49')})
# with open(record, 'rb') as pickle_file:
#     content = pickle.load(pickle_file)
#     df =  pd.DataFrame(list(content))
#     print(df)   








#*****************************************************************REST API Assignment *****************************************************************************
app.config['upload_folder'] = "D:\digi_try_fileupload"
#all User list
def project_api_routes(endpoints):
    @endpoints.route('/hello', methods=['GET'])
    def hello():
        res = 'Hello world'
        print("Hello world")
        return res

    # @endpoints.route("/user", methods=['GET'])
    # def find_all_people():
    #     collection = test_db.login
    #     user = collection.find() 
        
        
    #     return json.loads(json_util.dumps(user))

        
        
        # return json.loads(json_util.dumps(people_list_doc))
    @endpoints.route("/user/<id>")
    def user(id):
        collection = test_db.test
        user = collection.find_one({'_id':ObjectId(id)})

        return json.loads(json_util.dumps(user))




    @endpoints.route("/add", methods=['POST'])
    def add_user():
        
        collection = test_db.test
        req = request.get_json()
            
        # _json = request.json
        _password = request.json['password']
        _name = request.json['username']
        
        
        if _name and _password and request.method == 'POST':
            inserted_id = collection.insert_one({'password':_password,'name':_name}).inserted_id
            print(inserted_id)
            resp = jsonify("user added succesfully")
            resp.status_code = 200

            return resp
        else:
            return not_found()



    @endpoints.route("/add1", methods=['POST'])
    def add_am():
        
        collection = test_db.login
        data = request.get_json()
            
        # _json = request.json
        Name = data['name']
        
        date = data['date']
        print(data)
        
        
        
        
        
        if  request.method == 'POST':
            inserted_id = collection.insert_one({'companyName':Name,'date':date}).inserted_id
            print(inserted_id)
            resp = jsonify("user added succesfully")
            resp.status_code = 200

            return resp
        else:
            return not_found()



    @endpoints.route("/file", methods=['POST'])
    def add_file():
        
        collection = test_db.dqresults
        f = request.files['file']
        
        
        pandas_df = pd.read_csv(f, low_memory=False)
        pdf= pandas_df.fillna(0)

        # sdf = spark.createDataFrame(pandas_df.astype(str))

        # # sdf.printSchema()
        # sdf.show()
        # print(sdf.head())
        # svm = sns.heatmap(pandas_df.isnull(),cbar=False,cmap='viridis')
        vars_with_na = [var for var in pandas_df.columns if pandas_df[var].isnull().sum() > 0]

        # figure = svm.get_figure()    
        # figure.savefig('svm_conf.png',dpi=400)
        size = sys.getsizeof(pandas_df)
        res_size = size/1000000
        dataset_shape = pandas_df.shape
        def printinfo():
            temp = pd.DataFrame(index=pandas_df.columns)
            
            
            temp['null_count'] = pandas_df.isnull().sum()
            temp['unique_count'] = pandas_df.nunique()
            temp['duplicate_count'] =pandas_df.duplicated().sum() 
    
    
            return temp.values.tolist()
        
        
        inserted_id = collection.insert_one({'ColunmList': list(pandas_df.columns), 'dec':printinfo(), 'dataset_shape':dataset_shape, 'df_head':pdf.head().values.tolist(),'df_tail':pandas_df.tail().values.tolist(),
        'df_des':pandas_df.describe().values.tolist(), 'size': res_size }).inserted_id
        print(inserted_id)
        resp = jsonify("user added succesfully")
        resp.status_code = 200

        return resp
        
      
        
        


    @endpoints.route("/delete/<id>", methods=['DELETE'])        
    def delete_user(id):
        collection = test_db.test
        collection.delete_one({'_id':ObjectId(id)})
        resp = jsonify("deleted successfully")

        resp.status_code = 200
        return resp




    @endpoints.route("/update/<id>", methods=['PUT'])    
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

    @endpoints.errorhandler(404)        
    def not_found(error=None):
        message={
            'status':404,
            'message':'not found' + request.url
        }
        resp = jsonify(message)
        resp.status_code = 400

        return resp
    return endpoints




#******Business_logic



    


if __name__ == "__main__":
    app.run(debug=True)