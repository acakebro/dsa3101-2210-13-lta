import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc
import datetime


class RandomForestModel:
    def __init__(self, training, cam_lat_long):
        self.training = pd.read_csv(training)
        self.cam_lat_long = pd.read_csv(cam_lat_long)
        self.test_df = None
        self.model = self.__trainModel()

    def toDummy(self, data):
        data = data.drop(['Time', 'Date', 'Average_Speed',
                         'Vehicle_Count', 'Density', 'Incident'], axis=1)
        for col in data.dtypes[data.dtypes == "object"].index:
            for_dummy = data.pop(col)
            data = pd.concat(
                [data, pd.get_dummies(for_dummy, prefix=col)], axis=1)
        return data

    def __trainModel(self):
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
        self.test_df = pd.DataFrame(columns=list(train.columns))
        self.test_df = self.test_df.append(
            pd.Series(dtype='float64'), ignore_index=True)
        return model

    def __is_weekday(self, day):
        if day < 5:  # Monday(0) to Friday(4)
            return 1
        return 0

    def __time_in_range(self, start, end, x):
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end

    def __is_peak(self, time):
        peak_hours = [
            {"Start": datetime.time(8, 0, 0), "End": datetime.time(10, 0, 0)},
            {"Start": datetime.time(18, 0, 0),
             "End": datetime.time(20, 30, 0)},
        ]
        is_peak_bool = False
        for peak_hour in peak_hours:
            if is_peak_bool:
                return 1
            start, end = peak_hour.get("Start"), peak_hour.get("End")
            is_peak_bool = self.__time_in_range(start, end, time)
        return 0

    def predict(self, cam_id, road, date, time):
        day = datetime.datetime.strptime(date, "%d/%m/%Y").weekday()
        time = datetime.datetime.strptime(time, "%H:%M").time()
        is_weekday = self.__is_weekday(day)
        is_peak = self.__is_peak(time)
        cam_lat_long = self.cam_lat_long[self.cam_lat_long["CameraID"] == int(
            cam_id)]
        direction = "Direction_" + road.upper()
        test = self.test_df.copy()
        test.Camera_Id = int(cam_id)
        test.Latitude = cam_lat_long.iloc[0, 1]
        test.Longitude = cam_lat_long.iloc[0, 2]
        test.Is_Weekday = is_weekday
        test.Is_Peak = is_peak
        test[direction] = 1
        test = test.fillna(0)
        test_pred = self.model.predict(test)
        return test_pred[0]


# ----------------------------PIPELINE-----------------------------------------------
"""
model = RandomForestModel(
    "training_data/training_data.csv", "camera_id_lat_long.csv")
print(model.predict("2701", "Johor", "22/10/2022", "08:50"))
"""
