import json
import urllib
import urllib.request
from urllib.parse import urlparse
import httplib2 as http # external library
import pandas as pd
from datetime import datetime, timezone, timedelta
import zipfile
import os

def api_get_json(uri, path, type):
    if __name__ == "__main__":
        # authentication parameters
        headers = { 'AccountKey' : 'AO4qMbK3S7CWKSlplQZqlA==', 'accept' : 'application/json'} #this is by default

        # build query string & specify type of API call
        target = urlparse(uri + path)
        method = 'GET'
        body = ''

        h = http.Http() # get handle to http
        response, content = h.request(target.geturl(), method, body, headers)

        # handle response    to get datetime
        global datetime_str
        if datetime_str == '':
            date_obj = response['date'] # date & time in string
            datetime_gmt = datetime.strptime(date_obj, '%a, %d %b %Y %H:%M:%S %Z') # timezone: GMT (same as UTC)
            datetime_sgt = datetime_gmt.replace(tzinfo=timezone.utc).astimezone(tz=None)
            datetime_str = datetime_sgt.strftime('%Y_%m_%d_%H_%M')

        # create folder to store data
        global folder
        folder = os.path.join(parent_dir, datetime_str)
        if not os.path.isdir(folder):
            os.makedirs(folder)

        # get data from content
        jsonObj = json.loads(content) # dictonary
        data = jsonObj['value']
        if type == 'speed': # direct to download speedbands
            download_speedband(data, datetime_str)
        elif type == 'image':
            download_images(data)
        elif type == 'incidents':
            download_incidents(data, datetime_str)

def download_speedband(data, datetime):
    datetime_str = datetime
    df = pd.DataFrame(data)
    df['Location'] = df['Location'].apply(lambda x: x.split(' '))
    df[['StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude']] = pd.DataFrame(df['Location'].to_list())
    filename = '{datetime}_speedband.csv'.format(datetime=datetime_str)
    df.to_csv(os.path.join(folder, filename), index=False)

def download_images(data):
    url_link = data[0]['ImageLink']
    zipname = '_'.join(url_link.split('/')[3:5]).replace('-', '_')
    zipPath = os.path.join(folder, '%s.zip' % zipname)
    with zipfile.ZipFile(zipPath, mode='w') as img_zip:
        for i, dict in enumerate(data):
            link = dict['ImageLink']
            filename = link.split('/')[5].split('?')[0]
            url = urllib.request.urlopen(link)
            # img_name = os.path.basename(image_url)
            img_zip.writestr(filename, url.read())
        print(os.path.exists(zipPath))  # probing a zip file was written

def download_incidents(data, datetime):
    datetime_str = datetime
    df = pd.DataFrame(data)
    filename = '{datetime}_incidents.csv'.format(datetime=datetime_str)
    df.to_csv(os.path.join(folder, filename), index=False)


# -------------- MAKE API CALL --------------

# set path (if needed)
parent_dir = 'C:\\Users\\renac\\Downloads\\NUS\\Y3S1\\DSA3101\\project\\api_downloads'
os.chdir(parent_dir)

# api parameters
uri = 'http://datamall2.mytransport.sg' # resource URL
speed_path = '/ltaodataservice/TrafficSpeedBandsv2'
img_path = '/ltaodataservice/Traffic-Imagesv2'
incident_path = '/ltaodataservice/TrafficIncidents'

datetime_str = ''
api_get_json(uri, img_path, 'image')
api_get_json(uri, speed_path, 'speed')
api_get_json(uri, incident_path, 'incidents')