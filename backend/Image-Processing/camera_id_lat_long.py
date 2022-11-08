"""
Obtain latitude and longitude of the 87 traffic image cameras.
Stored in camera_id_lat_long.csv
"""
import json
import urllib
from urllib.parse import urlparse
import httplib2 as http # external library
import pandas as pd

# api parameters
uri = 'http://datamall2.mytransport.sg' # resource URL
path = '/ltaodataservice/Traffic-Imagesv2'

def api_get_json(uri, path) :
    if __name__ == "__main__":
        # authentication parameters
        headers = { 'AccountKey' : 'AO4qMbK3S7CWKSlplQZqlA==', 'accept' : 'application/json'} #this is by default

        # build query string & specify type of API call
        target = urlparse(uri + path)
        method = 'GET'
        body = ''

        h = http.Http() # get handle to http
        response, content = h.request(target.geturl(), method, body, headers)

        # get data from content
        jsonObj = json.loads(content) # dictonary
        data = jsonObj['value']
        df = pd.DataFrame(data)
        df.drop(columns=['ImageLink'], inplace=True)
        # print(df)

        df.to_csv('camera_id_lat_long.csv', index=False)

api_get_json(uri, path)





