# HyperETA

These are the program of the paper ***HyperETA: a Non-Deep-Learning Method for Estimated Time of Arrival***. 

Estimated Time of Arrival (ETA) that predicts a given GPS trajectory’s travel time has been widely used in route planning. 
We present a new machine learning algorithm, called HyperETA, for ETA prediction.
HyperETA is based on the Hypercube clustering method to measure the similarity among trajectories.
This program uses Cheng-Du taxi trajectories as a benchmark.

# The Environment :

This program run on python3.7. 
**conda_env.yml** have the list of required libraries.

# Usage:

```
python run_HyperETA.py
```
will show evaluated results (MAPE,RMSE,MAE)

```
python run_HyperETA_noDTW.py
```
will show the results not involve DTW.

# Data

## trajTrain.pickle

The trajectories model, includes 3 tables
* Hypercube series table : Preprocessed trajectories.
* Original trajectories table: Original GPS data.
* Mapping table : It map hypercubes to original trajectories.

## trajTest.pickle

Test data, includes 3 tables
* Hypercube series table : Preprocessed trajectories.
* Original trajectories table: Original GPS data.
* Mapping table : It map hypercubes to original trajectories.

