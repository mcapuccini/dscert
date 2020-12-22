import click
from sklearn.model_selection import train_test_split
import os
from azureml.core import Dataset
from azureml.core import Run
import numpy as np

@click.command()
@click.option("--out", type=str)
@click.option("--ds-name", type=str)
def experiment(out, ds_name):
    # Get the experiment run context and ws
    run = Run.get_context()
    ws = run.experiment.workspace

    # Prepare the dataset
    dataset = Dataset.get_by_name(workspace=ws, name=ds_name)
    data = dataset.to_pandas_dataframe()
    X, y = data.iloc[:,:-1].values, data.iloc[:,-1].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

    # Save the trained model
    os.makedirs(out, exist_ok=True)
    np.save(os.path.join(out, 'X_train.npy'), X_train)
    np.save(os.path.join(out, 'X_test.npy'), X_test)
    np.save(os.path.join(out, 'y_train.npy'), y_train)
    np.save(os.path.join(out, 'y_test.npy'), y_test)

    run.complete()

if __name__ == '__main__':
    experiment() # pylint: disable=no-value-for-parameter