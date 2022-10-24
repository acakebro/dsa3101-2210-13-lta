# Random Forest Model
import numpy as np
import matplotlib as mpl
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc
import pickle

# Reading of data
train = pd.read_csv("training_data/training_data.csv")

# Convert qualitative predictors to dummy variables
for col in train.dtypes[train.dtypes == "object"].index:
    for_dummy = train.pop(col)
    train = pd.concat([train, pd.get_dummies(for_dummy, prefix=col)], axis=1)

# extract response variabels
labels = train.pop("Jam")

# split dataset
x_train, x_test, y_train, y_test = train_test_split(train, labels, test_size=0.25)

# Begin Random Forest modelling
model = RandomForestClassifier()
model.fit(x_train, y_train)  # trained model

# Predicted response from validation dataset
y_pred = model.predict(x_test)

# Checking for accuracy
false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
roc_auc = auc(false_positive_rate, true_positive_rate)

# Finding the right estimator size for boostrapping
n_estimators = [1, 2, 4, 8, 16, 32, 64, 100, 200]
train_results = []
test_results = []
for estimator in n_estimators:
    rf = RandomForestClassifier(n_estimators=estimator, n_jobs=-1)
    rf.fit(x_train, y_train)
    train_pred = rf.predict(x_train)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_train, train_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    train_results.append(roc_auc)
    y_pred = rf.predict(x_test)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    test_results.append(roc_auc)


index = test_results.index(min(test_results))
best_n = n_estimators[index]

# Retraining of model with best_n
model = RandomForestClassifier(n_estimators=best_n)

# Fitting the whole training dataset into the model
model.fit(train, labels)  # use this model to predict income test dataset

# Save the model with pickle
pickle.dump(model, open("model.pkl", "wb"))