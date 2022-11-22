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

def salesforcast(endpoints):
    @endpoints.route("/Saleforcast", methods=['GET'])
    def sales_forcast():

        #*importing the pickel file********

        with open('D:\BK dev\python\python practices\digiverz_portal_API\saved_steps_salesforcast.pkl', 'rb') as file:
            data = pickle.load(file)
        forcast_loaded = data["model"]
        result = data["result"]
        y = data["y"]
        forcast_loaded = result.get_forecast(steps = 50)
        pred_ci = forcast_loaded.conf_int()

        ax = y.plot(label = 'observed', figsize = (14, 7))
        forcast_loaded.predicted_mean.plot(ax = ax, label = 'forecast')
        ax.fill_between(pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color = 'k', alpha = 0.25)
        ax.set_xlabel('Date')
        ax.set_ylabel('Furniture Sales')

        plt.legend()
        plt.show()
        plt.savefig(r"salesforcast.png",transparent=True)



        resp = jsonify("user inputs added succesfully")
        resp.status_code = 200

        return resp
    return endpoints