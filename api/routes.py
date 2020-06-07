from flask import Blueprint,Flask, request, jsonify
import numpy as np
import pandas as pd
import random
import math
import pickle


def open_file(chemin_csv,p):
    # p% of the lines
    # keep the header, then take only p% of lines
    # if random from [0,1] interval is greater than p, the row will be skipped
    df=pd.read_csv(chemin_csv,header=0,skiprows=lambda i: i>0 and random.random() > p,low_memory=False) 
    return df

df=open_file('data/full.csv',0.01)

account_api = Blueprint('account_api', __name__)

model = pickle.load(open('model.visg','rb'))

@account_api.route('/predict',methods=['POST'])
def predict():
    #Get the features
    res_form=request.form.values()
    final_features = [np.array(res_form)]
    res=model.predict(final_features)
    output=res[0]
    #apply inverse log1p : transf price in the model
    output=math.exp(output)-1
    return jsonify(output)


@account_api.route('/data_heatmap',methods=['GET'])
def data_heatmap():
    res=df[['valeur_fonciere','latitude','longitude']]
    return res.to_json()

@account_api.route('/data_graphique_avg_price_dep',methods=['GET'])
def data_graphique_avg_price_dep():
    res=df[['valeur_fonciere','code_departement']]
    res=res.groupby(['code_departement']).mean()
    return res.to_json()

@account_api.route('/data_graphique_avg_surface_dep',methods=['GET'])
def data_graphique_avg_surface_dep():
    res=df[['surface_terrain','code_departement']]
    res=res.groupby(['code_departement']).mean()
    return res.to_json()