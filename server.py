from flask import Flask, session, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
import csv

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app, supports_credentials=True)

# from simple_salesforce import Salesforce
#
# consumer_key = 'your_consumer_key'
# consumer_secret = 'your_consumer_secret'
# access_token_url = 'https://login.salesforce.com/services/oauth2/token'
# redirect_uri = 'http://localhost:5000/callback'
# authorize_url = 'https://login.salesforce.com/services/oauth2/authorize'
# app = Flask(__name__)
#
# @app.route('/login')
# def login():
#     url = "%s?response_type=code&client_id=%s&redirect_uri=%s" % (authorize_url, consumer_key, redirect_uri)
#     return redirect(url)
#
#
# @app.route('/callback')
# def callback():
#     code = request.args.get('code')
#     data = {
#         'grant_type': 'authorization_code',
#         'redirect_uri': redirect_uri,
#         'code': code,
#         'client_id': consumer_key,
#         'client_secret': consumer_secret
#     }
#     headers = {
#         'content-type': 'application/x-www-form-urlencoded'
#     }
#     req = requests.post(access_token_url, data=data, headers=headers)
#     response = req.json()
#
#     sf = Salesforce(instance_url=response['instance_url'], session_id=response['access_token'])
#
#     #Now you can make your calls to the Salesforce api using the sf object. For more information: https://github.com/simple-salesforce/simple-salesforce
#
#
#     return "ok, connected to Salesforce"


# Read data from file 'filename.csv'
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later)
df = pd.read_csv("Contact_2_1_1.csv")

@app.route('/getstate/<state>', methods=['GET'])
def get_state(state):
    if df.loc[df['OtherState'] == state].empty:
        return jsonify({"Message": "No Such State Exists"})
    else:
        states = df.loc[df['OtherState'] == state]['OtherCity'].tolist()
        return jsonify({"cities" : states})

@app.route('/numcities/<state>',methods=['GET'])
def num_of_cities(state):
    if df.loc[df['OtherState'] == state].empty:
        return jsonify({"Message": "No Such State Exists"})
    else:
        num_cities = len(df.loc[df['OtherState'] == state]['OtherCity'].tolist())
        return jsonify({"num_of_cities" : num_cities})

@app.route('/addcity/<state>', methods=['POST'])
def add_city(state):
    if df.loc[df['OtherState'] == state].empty:
       return jsonify({"Message" : "No Such State Exists"})
    else:
        row = []
        for col in df.columns:
            row.append(request.form[str(col)])
        try:
            with open(r'Contact_2_1_1.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(row)
                print('Success')
        except Exception as e:
            print(str(e))
            print('Unable to Write CSV')
        return request.form['AccountId']

if __name__ == "__main__":
    app.run(host="localhost", debug=True)