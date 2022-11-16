from pyexpat import model
from flask import Flask, render_template, request
import numpy as np
import pickle
import requests


# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "0-zgnSwLwHnXYQBaeXUguHLwv2X7zN0kkDaTdPGdaR8f"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)



@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        sg = float(request.form['sg'])
        htn = float(request.form['htn'])
        hemo = float(request.form['hemo'])
        dm = float(request.form['dm'])
        al = float(request.form['al'])
        appet = float(request.form['appet'])
        rc = float(request.form['rc'])
        pc = float(request.form['pc'])

        values = [[sg, htn, hemo, dm, al, appet, rc, pc]]

        payload_scoring = {"input_data": [{"field": [[sg, htn, hemo, dm, al, appet, rc, pc]],"values": values}]}

        response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/3a87143a-e956-4c61-8fde-9b2b904ce0a8/predictions?version=2022-11-02', json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
        print("response_scoring ")

        predictions = response_scoring.json()
        prediction = model.predict(values)
        print('Hiiiiiiiiiiiiii', prediction)
    
        
        return render_template('result.html', predict=predict)


if __name__ == "__main__":
    app.run(debug=True)
