from pyspark.sql.functions import when, lit, regexp_replace, substring, to_timestamp, to_date, col
from pyspark.sql.types import DoubleType, StringType
from digiverz_portal_API.FlaskRestAPI import test_db
from pyspark.sql.types import *
from sklearn.preprocessing import LabelEncoder
from pyspark.sql import SparkSession
import pyspark
import sys

import seaborn as sns
from pymongo import MongoClient 
import pprint
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import sklearn
import numpy as np
import pickle
import pandas as pd
import math
from bson.objectid import ObjectId
from flask import jsonify, request
from flask_cors import CORS, cross_origin
from bson import json_util
import json
import bson

import datetime
from datetime import datetime

from flask import Flask
from http import client
from unittest import result
from dotenv import load_dotenv, find_dotenv


from pycaret.datasets import get_data
from pycaret.regression import *


import matplotlib
matplotlib.use('Agg')

load_dotenv(find_dotenv())



def algo_reg_endponts(endpoints):
    @endpoints.route("/post_col_name_reg", methods=['POST'])
    def algo_analyze_result_reg():
        collection = test_db.algo_results_reg
        _req = request.get_json()
        col_name = _req['colunm']
        pycaret_opt = _req['pycaretopt']
        print("im printing options")
        print(pycaret_opt)

        

        f = pd.read_pickle("./algo.pkl")

        f.to_csv(r'file.csv')

        dataset = get_data('file')

       
        

        
            

        data = dataset.sample(frac=0.95, random_state=786)
        data_unseen = dataset.drop(data.index)
        data.reset_index(inplace=True, drop=True)
        data_unseen.reset_index(inplace=True, drop=True)
        print('Data for Modeling: ' + str(data.shape))
        print('Unseen Data For Predictions: ' + str(data_unseen.shape))

        exp_clf101 = setup(data=data, target= col_name)
        best_model = compare_models()
        best_model = pull()
        algo_result = best_model.values.tolist()
        algo_result_modified = best_model.to_json(orient='records')
        inserted_id = collection.insert_one({
            'analyzed_data':
            algo_result,
            'analyzed_data_modified':algo_result_modified
        }).inserted_id
        print(inserted_id)
        resp = jsonify("OK")
        resp.status_code = 200
        
        return resp

    @endpoints.route("/algoresultsreg", methods=['GET'])
    def algo_results_reg():
        
        
        collection = test_db.algo_results_reg
        algo_results = collection.find()
        resp = jsonify("Colunm names")
        resp.status_code = 200  
        return json.loads(json_util.dumps(algo_results))    

    
    return endpoints