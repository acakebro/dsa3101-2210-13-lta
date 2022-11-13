"""
Retrieve raw LTA traffic images, speedbands and incidents from LTA DataMall. 
Data is stored in 'assets' folder, previous data will be cleared before the API calls are made.
"""
import json
import urllib
import urllib.request
from urllib.parse import urlparse
import httplib2 as http  # external library
import pandas as pd
# from datetime import datetime, timezone
import os
import shutil


class ApiCall:
    def __init__(self, parent_dir):
        self.parent_dir = parent_dir
        os.chdir(parent_dir)
        self.folder = os.path.join(self.parent_dir, "assets") # folder where data retrieve are stored
        if os.path.isdir(self.folder):
            shutil.rmtree(self.folder) # clear old data from folder before making api call
        os.makedirs(self.folder)

    def api_get_json(self, uri, path):
        """
        Makes request to retrive data from LTA DataMall.
        """
        # authentication parameters
        headers = {
            "AccountKey": "AO4qMbK3S7CWKSlplQZqlA==",
            "accept": "application/json",
        }  # this is by default

        # build query string & specify type of API call
        target = urlparse(uri + path)
        method = "GET"
        body = ""

        h = http.Http()  # get handle to http
        response, content = h.request(target.geturl(), method, body, headers) # retrieve data

        # get data from content
        jsonObj = json.loads(content)  # dictonary
        data = jsonObj["value"]
        return data

    def download_speedband(self):
        """
        Retrieve speedband data from LTA DataMall. Location is split into start latitude & longitude and end latitude & longitude (of type float).
        Store as csv in assets folder.
        """
        uri = "http://datamall2.mytransport.sg"  # resource URL
        speed_path = "/ltaodataservice/TrafficSpeedBandsv2"
        data = self.api_get_json(uri, speed_path)
        df = pd.DataFrame(data)

        df['AvgSpeed'] = df['SpeedBand'].apply(
            lambda x: x * 10 - 4.5)

        df["Location"] = df["Location"].apply(lambda x: x.split(" "))
        df[
            ["StartLatitude", "StartLongitude", "EndLatitude", "EndLongitude"]
        ] = pd.DataFrame(df["Location"].to_list())
        df = df.astype(
            {
                "StartLatitude": "float",
                "StartLongitude": "float",
                "EndLatitude": "float",
                "EndLongitude": "float",
            }
        )
        # average latitude, longitude of stretch of road
        df["AvgLat"] = (df.StartLatitude + df.EndLatitude) / 2
        df["AvgLon"] = (df.StartLongitude + df.EndLongitude) / 2

        # save file
        filename = "speedbands.csv"
        df.to_csv(os.path.join(self.folder, filename), index=False)

    def download_images(self):
        """
        Retrieves traffic images of 87 cameras from LTA DataMall.
        Store images in assets folder.
        """
        uri = "http://datamall2.mytransport.sg"  # resource URL
        img_path = "/ltaodataservice/Traffic-Imagesv2"
        data = self.api_get_json(uri, img_path)
        for i, dict in enumerate(data):
            link = dict["ImageLink"]
            filename = link.split("/")[5].split("?")[0]
            urllib.request.urlretrieve(
                link, os.path.join(self.folder, filename))

    def download_incidents(self):
        """
        Retrieves traffic incidents data from LTA DataMall.
        Store as csv in assets folder.
        """
        uri = "http://datamall2.mytransport.sg"  # resource URL
        incident_path = "/ltaodataservice/TrafficIncidents"
        data = self.api_get_json(uri, incident_path)
        df = pd.DataFrame(data)
        filename = "incidents.csv"
        df.to_csv(os.path.join(self.folder, filename), index=False)

    def clear_data(self):
        shutil.rmtree(self.folder)
