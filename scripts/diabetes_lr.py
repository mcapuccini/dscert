import click
from azureml.core import Run
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import os
import joblib

@click.command()
@click.option("--reg-rate", type=float, default=0.1)
def experiment(reg_rate):
    # Get the experiment run context
    run = Run.get_context()

    # Prepare the dataset
    data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv')
    X, y = data.iloc[:,:-1].values, data.iloc[:,-1].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

    # Train a logistic regression model
    model = LogisticRegression(C=1/reg_rate, solver="liblinear").fit(X_train, y_train)

    # calculate accuracy
    y_hat = model.predict(X_test)
    acc = np.average(y_hat == y_test)
    run.log('Accuracy', np.float(acc))

    # Save the trained model
    os.makedirs('outputs', exist_ok=True)
    joblib.dump(value=model, filename='outputs/diabetes.pkl')

    run.complete()

if __name__ == '__main__':
    experiment()