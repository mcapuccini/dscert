import click
from sklearn.model_selection import train_test_split
import os
from azureml.core import Dataset
from azureml.core import Run
import numpy as np
from sklearn.linear_model import LogisticRegression

@click.command()
@click.option("--split-dir", type=str)
@click.option("--reg-rate", type=float, default=0.1)
def experiment(split_dir, reg_rate):
    # Get the experiment run context
    run = Run.get_context()

    # Retrieve DS
    X_train = np.load(os.path.join(split_dir, 'X_train.npy'))
    X_test = np.load(os.path.join(split_dir, 'X_test.npy'))
    y_train = np.load(os.path.join(split_dir, 'y_train.npy'))
    y_test = np.load(os.path.join(split_dir, 'y_test.npy'))

    # Train a logistic regression model
    model = LogisticRegression(C=1/reg_rate, solver="liblinear").fit(X_train, y_train)

    # calculate accuracy
    y_hat = model.predict(X_test)
    acc = np.average(y_hat == y_test)
    run.log('Accuracy', np.float(acc))

    run.complete()

if __name__ == '__main__':
    experiment() # pylint: disable=no-value-for-parameter