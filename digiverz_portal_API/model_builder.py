
from typing import Collection
from urllib import request
from digiverz_portal_API.FlaskRestAPI import test_db
import matplotlib.pyplot as plt

import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder
#from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import json
from bson import json_util
from flask import jsonify, request
import numpy as np


def model_builder_endpoint(endpoints): 
    @endpoints.route("/user", methods=['GET'])
    def find_all_people():
        collection = test_db.login
        user = collection.find() 
        
        
        return json.loads(json_util.dumps(user))

    @endpoints.route("/modelBuilder", methods=['POST','GET'])
    def model_builder_pickel():

        #*importing the pickel file********

        with open('D:\BK dev\python\python practices\digiverz_portal_API\saved_steps.pkl', 'rb') as file:
            data = pickle.load(file)
        df = data["df"]
        fig, ax = plt.subplots(1,1, figsize=(12, 7))
        df.boxplot('Salary', 'Country', ax=ax)
        plt.suptitle('Salary (US$) v Country')
        plt.title('')
        plt.ylabel('Salary')
        plt.xticks(rotation=90)
        plt.savefig("squares.png")
        
        #*geting value from the client************

        collection = test_db.modelbuilder
        _req = request.get_json()
        _country = _req['country']
        _degree = _req['degree']
        _exp = _req['exp']
        X = np.array([[_country, _degree, _exp ]])


        regressor_loaded = data["model"]
        le_country = data["le_country"]
        le_education = data["le_education"]
        X[:, 0] = le_country.transform(X[:,0])
        X[:, 1] = le_education.transform(X[:,1])
        X = X.astype(float)
        
        y_pred = regressor_loaded.predict(X)
        
        if  request.method == 'POST':
            inserted_id = collection.insert_one({ 'country': _country,'degree':  _degree,'exp': _exp, 'result':y_pred}).inserted_id
            print(inserted_id)
            resp = jsonify("user inputs added succesfully")
            resp.status_code = 200

            return resp
        return json.loads(json_util.dumps(y_pred))    

       
    return endpoints