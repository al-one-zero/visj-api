import pickle
import pandas as pd
import numpy as np
import random
import pickle

chemin_csv='data/full.csv'

p = 0.01 # 1% of the lines

# keep the header, then take only 1% of lines
# if random from [0,1] interval is greater than 0.01 the row will be skipped

df=pd.read_csv(chemin_csv,header=0,skiprows=lambda i: i>0 and random.random() > p,index_col=0,low_memory=False)

#preprocessing

#drop features with to 60% null values 
df=df[df.columns[df.isnull().mean() < 0.5]]

#drop column with same signification (code/signification) 
column_to_drop=['type_local','nature_culture','nom_commune']
df.drop(column_to_drop, axis=1, inplace=True)

#drop column adress, we'll be working with longitude/latitude 
column_to_drop=['adresse_numero','adresse_nom_voie','adresse_code_voie']
df.drop(column_to_drop, axis=1, inplace=True)

#drop column not useful for our context
column_to_drop=['id_parcelle','date_mutation','numero_disposition']
df.drop(column_to_drop, axis=1, inplace=True)

#drop rows where 'valeur_fonciere' is NaN
df = df.dropna(axis=0, subset=['valeur_fonciere'])

#drop nombre_pieces_principales cause of the big correlation with code_type_local 
column_to_drop=['nombre_pieces_principales']
df.drop(column_to_drop, axis=1, inplace=True)

#fill miss values
df["code_nature_culture"] = df["code_nature_culture"].fillna("None")

for col in ('code_postal','longitude','latitude','surface_terrain','code_type_local'):
    df[col] = df.groupby("code_departement")[col].transform(lambda x: x.fillna(x.median()))

#drop rows where 'code_type_local' is NaN
df = df.dropna(axis=0, subset=['code_type_local'])

#Transformation
df["code_postal"]=df["code_postal"].apply(str)
df["code_type_local"]=df["code_type_local"].apply(str)

# We use the numpy fuction log1p which  applies log(1+x) to all elements of the column
df["valeur_fonciere"] = np.log1p(df["valeur_fonciere"])

df = pd.get_dummies(df)

#modeling
y=df['valeur_fonciere']
X=df.drop('valeur_fonciere', axis=1)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

from sklearn.linear_model import RandomForestRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

#PCA
pca = make_pipeline(RobustScaler(), PCA(n_components=8))
pca.fit(X_train)
X_train, X_test = pca.transform(X_train), pca.transform(X_test)

#Model training
forest = make_pipeline(RobustScaler(), RandomForestRegressor())
forest.fit(X_train, y_train)

<<<<<<< HEAD
pickle.dump(forest, open('model.visg','wb'))
=======
#ENet.fit(X_train, y_train)
#Using Lasso nets slightly better results
#Lasso.fit(X_train, y_train)
#Using RANSAC Regressor nets even better results
ransac.fit(X_train, y_train)

pickle.dump(Lasso,open('api/model.visg','wb'))
>>>>>>> d67dc0eca7d8909b36fd4c741366419c049d0e78
