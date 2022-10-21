
from array import array
from turtle import color
from typing import Collection
from urllib import request
from digiverz_portal_API.FlaskRestAPI import test_db
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import bson
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
    @endpoints.route("/mbresult", methods=['GET'])
    def find_all_people():
        collection = test_db.modelbuilder
        user = collection.find() 
        
        
        return json.loads(json_util.dumps(user))

    @endpoints.route("/modelBuilder", methods=['POST','GET'])
    def model_builder_pickel():

        #*importing the pickel file********

        with open('D:\BK dev\python\python practices\digiverz_portal_API\saved_steps.pkl', 'rb') as file:
            data = pickle.load(file)
        df = data["df"]
        fig, ax = plt.subplots(1,1, figsize=(12, 7))
        plt.bar('Salary', 'Country', color='red', width=0.5)
        plt.suptitle('Salary (US$) v Country')
        plt.title('')
        plt.ylabel('Salary')
        plt.xticks(rotation=90)
        plt.savefig(r"D:\BK dev\digitech\DigitechPortal\digiverz\src\assests\squares.png", transparent=True)
        
        
        
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

        mb_result = np.array_str(y_pred)
        data = df["Country"].value_counts()

        fig1, ax1 = plt.subplots()
        ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
        ax1.axis("equal")
        
        plt.savefig(r"D:\BK dev\digitech\DigitechPortal\digiverz\src\assests\squares1.png",transparent=True)
        imgmb = {
            "imagedata" : bson.Binary(pickle.dumps(fig)),
            "contenttype": "image/png"
        }
        if  request.method == 'POST':
            inserted_id = collection.insert_one({ 'country': _country,'degree':  _degree,'exp': _exp, 'result':mb_result,  "binary_field": imgmb }).inserted_id
            print(inserted_id)
            resp = jsonify("user inputs added succesfully")
            resp.status_code = 200

            return resp
        return json.loads(json_util.dumps(mb_result))

       
    return endpoints