import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc


class RandomForestModel:
    def __init__(self, training):
        self.training = pd.read_csv(training)
        self.model = self.trainModel()

    def toDummy(self, data):
        time = data.pop("Time")  # remove time
        date = data.pop("Date")
        for col in data.dtypes[data.dtypes == "object"].index:
            for_dummy = data.pop(col)
            data = pd.concat(
                [data, pd.get_dummies(for_dummy, prefix=col)], axis=1)
        return data

    def trainModel(self):  # no pickle
        train = self.training
        labels = train.pop("Jam")
        train = self.toDummy(train)
        x_train, x_test, y_train, y_test = train_test_split(
            train, labels, test_size=0.25
        )
        model = RandomForestClassifier()
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        false_positive_rate, true_positive_rate, thresholds = roc_curve(
            y_test, y_pred)
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
        model.fit(train, labels)
        return model

    def predict(self, test_dir):
        test = pd.read_csv(test_dir)
        result = test.copy()
        test = self.toDummy(test)
        test_pred = self.model.predict(test)
        result["Jam"] = test_pred
        return result


# ----------------------------PIPELINE-----------------------------------------------
"""
model = RandomForestModel('training_data/training_data.csv')
print(model.predict('training_data/test.csv'))
print(model.predict('training_data/test2.csv'))
"""
