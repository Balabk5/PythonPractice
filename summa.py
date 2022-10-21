import pickle
import pandas as pd
import matplotlib.pyplot as plt

with open('D:\BK dev\python\python practices\digiverz_portal_API\saved_steps.pkl', 'rb') as file:
            data = pickle.load(file)
            df = data["df"]
            print(df)
            df.plot(kind='bar', x='Edlevel', y='Salary')
            plt.show()