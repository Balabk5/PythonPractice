
from digiverz_portal_API.FlaskRestAPI import test_db



import pandas as pd
from sklearn.preprocessing import LabelEncoder
#from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import json
from bson import json_util



def model_builder_endpoint(endpoints):
    @endpoints.route('/model')
    def model_builder_function():
        collection =test_db.salarydataset
        user = collection.find() 
        df = pd.DataFrame(list(user))
        del df["_id"]
        df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
        df = df.rename({"ConvertedComp": "Salary"}, axis=1)
        df = df.dropna()
        df.isnull().sum()
        df = df[df["Employment"] == "Employed full-time"]
        df = df.drop("Employment", axis=1)
        def shorten_categories(categories, cutoff):
            categorical_map = {}
            for i in range(len(categories)):
                if categories.values[i] >= cutoff:
                    categorical_map[categories.index[i]] = categories.index[i]
                else:
                    categorical_map[categories.index[i]] = 'Other'
            return categorical_map
        country_map = shorten_categories(df.Country.value_counts(), 400)
        df['Country'] = df['Country'].map(country_map)
        

        return print(df.Country.value_counts())
        
    @endpoints.route("/user", methods=['GET'])
    def find_all_people():
        collection = test_db.login
        user = collection.find() 
        
        
        return json.loads(json_util.dumps(user))
    return endpoints