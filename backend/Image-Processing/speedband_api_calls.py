import json
import urllib
from urllib.parse import urlparse
import httplib2 as http # external library
import pandas as pd
from datetime import datetime, timezone
# import requests
# import os
# import time

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

        # handle response to get datetime
        date_obj = response['date'] # date & time in string
        datetime_gmt = datetime.strptime(date_obj, '%a, %d %b %Y %H:%M:%S %Z') # timezone: GMT (same as UTC)
        datetime_sgt = datetime_gmt.replace(tzinfo=timezone.utc).astimezone(tz=None)
        datetime_str = datetime_sgt.strftime('%Y_%m_%d_%H_%M')

        # get data from content
        jsonObj = json.loads(content) # dictonary
        data = jsonObj['value']
        df = pd.DataFrame(data)
        df['Location'] = df['Location'].apply(lambda x: x.split(' '))
        return df, datetime_str

# api parameters
uri = 'http://datamall2.mytransport.sg' # resource URL
speed_path = '/ltaodataservice/TrafficSpeedBandsv2'

df, datetime_str = api_get_json(uri, speed_path)
filename = '{datetime}.csv'.format(datetime=datetime_str)
df.to_csv(filename, index=False)