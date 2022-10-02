import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression

# Prepping data, deleting species without enough samples
data = gpd.read_file("fish_data/ds195.shp")
data.drop(data[data["WEIGHT"] == 0.0].index, inplace = True)
data.drop(data[data["LENGTH"] > 1000].index, inplace = True)
data.drop(data[data["CNAME"] == "Smallmouth Bass"].index, inplace = True)
data.drop(data[data["CNAME"] == "Riffle Sculpin"].index, inplace = True)
data.drop(data[data["CNAME"] == "California Roach"].index, inplace = True)
data.drop(data[data["CNAME"] == "Sacramento Pikeminnow"].index, inplace = True)
data.drop(data[data["CNAME"] == "Goldfish"].index, inplace = True)
data.drop(data[data["CNAME"] == "Cutthroat Trout"].index, inplace = True)
data.drop(data[data["CNAME"] == "Redear Sunfish"].index, inplace = True)

# Grouping species to accomodate spei=cies identifier
for ind in data.index:
    data["CNAME"][ind]

    if data["CNAME"][ind] == "Brook Trout" or data["CNAME"][ind] == "Golden Trout" or data["CNAME"][ind] == "Rainbow Trout" or data["CNAME"][ind] == "Brown Trout":
        data["CNAME"][ind] = "Trout"

    if data["CNAME"][ind] == "Largemouth Bass" or data["CNAME"][ind] == "Spotted Bass":
        data["CNAME"][ind] = "Bass"

species = data["CNAME"].unique()
species_models = {}

for specie in species:
    specie_data = data[data["CNAME"] == specie]

    X = specie_data["LENGTH"]
    y = specie_data["WEIGHT"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # X_seq = np.linspace(X_train.min(), X_train.max(),300). reshape(-1,1)

    # degree = 3
    # polyreg = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    # polyreg.fit(pd.DataFrame.from_dict({'X': X_train.to_numpy()}), pd.DataFrame.from_dict({'y': y_train.to_numpy()}))
    # print(polyreg.steps)

    # linear = LinearRegression()
    # linear.fit(X_train, y_train)
    # linear.

    # species_models[specie] = polyreg

    # with open("fish model of " + specie + ".pickle", "wb") as f:
    #     pickle.dump(polyreg, f)

    pickle_in = open("MAIS-Hacks-2022/find_my_fish/data/fish model of " + specie + ".pickle", "rb")
    species_models[specie] = pickle.load(pickle_in)

    # r2_score = species_models[specie].score(pd.DataFrame.from_dict({'X': X_test.to_numpy()}), pd.DataFrame.from_dict({'y': y_test.to_numpy()}))
    # print(r2_score)

    # joblib.dump(polyreg, "fish_model" + specie + ".joblib")