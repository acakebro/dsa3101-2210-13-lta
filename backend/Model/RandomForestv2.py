import numpy as np
import matplotlib as mpl
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc


class RandomForestModel:
    def __init__(self, training, test):
        self.training = pd.read_csv("training_data.csv")
        self.test = pd.read_csv("test_data.csv")

    def toDummy(self, data):
        time = self.training.pop("Time")  # remove time
        # date = self.training.pop("Date")
        for col in data.dtypes[data.dtypes == "object"].index:
            for_dummy = data.pop(col)
            data = pd.concat([data, pd.get_dummies(for_dummy, prefix=col)], axis=1)

    def getModel(self):  # no pickle
        labels = self.training.pop("Jam")
        x_train, x_test, y_train, y_test = train_test_split(
            self.training, labels, test_size=0.25
        )
        model = RandomForestClassifier()
        model.fit = RandomForestClassifier()
        y_pred = model.predict(x_test)
        false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
        roc_auc = auc(false_positive_rate, true_positive_rate)

        n_estimators = [1, 2, 4, 8, 16, 32, 64, 100, 200]
        train_results = []
        test_results = []
        for estimator in n_estimators:
            rf = RandomForestClassifier(n_estimators=estimator, n_jobs=-1)
            rf.fit(x_train, y_train)
            train_pred = rf.predict(x_train)
            false_positive_rate, true_positive_rate, thresholds = roc_curve(
                y_train, train_pred
            )
            roc_auc = auc(false_positive_rate, true_positive_rate)
            train_results.append(roc_auc)
            y_pred = rf.predict(x_test)
            false_positive_rate, true_positive_rate, thresholds = roc_curve(
                y_test, y_pred
            )
            roc_auc = auc(false_positive_rate, true_positive_rate)
            test_results.append(roc_auc)

        index = test_results.index(min(test_results))
        best_n = n_estimators[index]
        model = RandomForestClassifier(n_estimators=best_n)
        model.fit(self.training, labels)
        # pickle.dump(model, open("model.pkl", "wb"))

    def predict_(self):
        copy = self.test.copy()
        testTime = self.test.pop("Time")
        testDate = self.test.pop("Date")
        self.toDummy(self.test)
        test_pred = self.getModel().predict(self.test)
        copy["Jam"] = test_pred
        copy.to_csv("Final_output.csv")


# ----------------------------PIPELINE-----------------------------------------------


# Loading of datasets
train = pd.read_csv("training_data.csv")

# Removing of time column
time = train.pop("Time")

# converting of qualitative variables to dummy variables for train
for col in train.dtypes[train.dtypes == "object"].index:
    for_dummy = train.pop(col)
    train = pd.concat([train, pd.get_dummies(for_dummy, prefix=col)], axis=1)

# Pop Jam to labels for training split
labels = train.pop("Jam")

# split dataset
x_train, x_test, y_train, y_test = train_test_split(train, labels, test_size=0.25)

# Begin Random Forest modelling
model = RandomForestClassifier()
model.fit(x_train, y_train)  # trained model
y_pred = model.predict(x_test)

# accuracy
false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
roc_auc = auc(false_positive_rate, true_positive_rate)
# roc_auc

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

# Retraining of model with best_n and full training dataset
model = RandomForestClassifier(n_estimators=best_n)
model.fit(train, labels)  # use this model to predict income test dataset

# Saving the model to pickle
pickle.dump(model, open("model.pkl", "wb"))

# ---------------------------------------------------------------

# Loading the model from the pickle
model = pickle.load(open("model.pkl", "rb"))
test = pd.read_csv("test_data.csv")
copy = test.copy()
testTime = test.pop("Time")

# Converting of qualitative predictors to dummy variables in test
for col in test.dtypes[test.dtypes == "object"].index:
    for_dummy = test.pop(col)
    test = pd.concat([test, pd.get_dummies(for_dummy, prefix=col)], axis=1)

# predicting on test dataset
test_pred = model.predict(test)
copy["Jam"] = test_pred
copy.to_csv("Final_output.csv")
