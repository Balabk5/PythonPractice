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
import statsmodels.api as sm
import datetime
from datetime import datetime
from dateutil import relativedelta
plt.style.use('fivethirtyeight')
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'

def salesforcast(endpoints):
    @endpoints.route("/Saleforcast", methods=['GET'])
    def sales_forcast():

        #*importing the pickel file********

        



        resp = jsonify("user inputs added succesfully")
        resp.status_code = 200

        return resp

    @endpoints.route("/sales_date", methods=['POST'])
    def Salesforecast_date():
        collection = test_db.sales_results
        _req = request.get_json()
        # end_date = _req['value']
        end_date = _req['date']
        start_date = '2015-01-01'
        s_datetime_object = datetime.strptime(start_date, '%Y-%m-%d').date()
        datetime_object = datetime.strptime(end_date, '%Y-%m-%d').date()
            
        # s_datetime_object = datetime.strptime(start_date, '%Y-%m-%d')
        # datetime_object = datetime.strptime(end_date, '%Y-%m-%d')

        # pycaret_opt = _req['pycaretopt']
        # print("im printing options")
        # print(pycaret_opt)
        

        print("im printing the date")
        print('\n')
        print(datetime_object)
        print(s_datetime_object)
        print("im printing types of dates the date")
        print('\n')
        print("sdate",type(s_datetime_object))
        print("e_date",type(datetime_object))
      
        delta = relativedelta.relativedelta(datetime_object, s_datetime_object)
        res_months = delta.months + (delta.years * 12) + 1
        # delta =  datetime_object - s_datetime_object
        # months = delta.months
        print("im printing difference btw the date")
        print('\n')

        print(res_months)

        print(res_months)

        with open('D:\BK dev\python\python practices\digiverz_portal_API\saved_steps_salesforcast.pkl', 'rb') as file:
            data = pickle.load(file)
        
        result = data["result"]
        y = data["y"]
        forcast_loaded = result.get_forecast(steps = res_months)
        pred_ci = forcast_loaded.conf_int()

        ax = y.plot(label = 'observed', figsize = (14, 7))
        forcast_loaded.predicted_mean.plot(ax = ax, label = 'forecast')
        ax.fill_between(pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color = 'k', alpha = 0.25)
        ax.set_xlabel('Date')
        ax.set_ylabel('Furniture Sales')

        plt.legend()
        
        plt.savefig(r"D:\BK dev\digitech\DigitechPortal\digiverz\src\assests\features\salesforcast.png")
        plt.clf()
        
        decomposition = sm.tsa.seasonal_decompose(y, model = 'additive')
        fig = decomposition.plot()
        
        plt.savefig(r"D:\BK dev\digitech\DigitechPortal\digiverz\src\assests\features\salesforcast_decomposition.png")
        plt.clf()
        
        resp = jsonify("OK")
        resp.status_code = 200
        
        return resp
    return endpoints