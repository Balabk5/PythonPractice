from fileinput import filename
from msilib.schema import File
from digiverz_portal_API.FlaskRestAPI import test_db
import json
from bson import json_util
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
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
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
from datetime import datetime

#*algo analyze
from pycaret.datasets import get_data
from pycaret.classification import *

glob_file = ''

def algo_analyze_endpoints(endpoints):

    @endpoints.route("/algofile", methods=['POST'])
    def add_file_algo_analyze():

        f = request.files['file']
        global glob_file
        glob_file = f
        collection = test_db.algocollist
        

        pandas_df = pd.read_csv(f, low_memory=False, encoding='unicode_escape')
        pandas_df.to_pickle("./algo.pkl")
         #*size and shape of df
        size = sys.getsizeof(pandas_df)
        res_size = size/1000000
        dataset_shape = pandas_df.shape
        
        inserted_id = collection.insert_one({
            'collist': list(pandas_df.columns),
            'size': res_size,
            'dataset_shape':dataset_shape,
            'file_name':f.filename
        }).inserted_id
        print(inserted_id)
        resp = jsonify("user added succesfully")
        resp.status_code = 200

        return resp

    @endpoints.route("/algocolunmnames", methods=['GET'])
    def algo_colunm_name():
        
        
        collection = test_db.algocollist
        find_all_col_from_collection = collection.find()
        resp = jsonify("Colunm names")
        resp.status_code = 200
        return json.loads(json_util.dumps(find_all_col_from_collection))

    @endpoints.route("/getcolnameforalgo", methods=['POST'])
    def algo_analyze_result():
        collection = test_db.algoanalyze
        _req = request.get_json()
        col_name = _req['colunm']
        
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
        inserted_id = collection.insert_one({
            'analyzed_data':
            algo_result,
            
        }).inserted_id
        print(inserted_id)
        resp = jsonify("user added succesfully")
        resp.status_code = 200

        return resp

    @endpoints.route("/algoresults", methods=['GET'])
    def algo_results():
        
        
        collection = test_db.algoanalyze
        algo_results = collection.find()
        resp = jsonify("Colunm names")
        resp.status_code = 200
        return json.loads(json_util.dumps(algo_results))        

    return endpoints