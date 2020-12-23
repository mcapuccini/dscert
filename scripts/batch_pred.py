# Create entry script
import os
import json
import joblib
import pandas as pd
from azureml.core.model import Model

# Called when the service is loaded
def init():
    global model
    # Get the path to the registered model file and load it
    model_path = Model.get_model_path('diabetes_model')
    model = joblib.load(model_path)

# Called when a request is received
def run(mini_batch):
    # Reshape into a 2-dimensional array for model input
    prediction = model.predict(mini_batch.iloc[:,:-1].values.reshape(1, -1))[0]
    return pd.DataFrame([prediction])