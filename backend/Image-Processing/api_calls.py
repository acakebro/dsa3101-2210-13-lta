import json
import urllib
import urllib.request
from urllib.parse import urlparse
import httplib2 as http # external library
import pandas as pd
from datetime import datetime, timezone
import zipfile
import os

class ApiCall():
    def __init__(self, parent_dir):
        self.parent_dir = parent_dir
        os.chdir(parent_dir)
        self.datetime_str = ''

    def api_get_json(self, uri, path):
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
            if self.datetime_str == '':
                date_obj = response['date'] # date & time in string
                datetime_gmt = datetime.strptime(date_obj, '%a, %d %b %Y %H:%M:%S %Z') # timezone: GMT (same as UTC)
                datetime_sgt = datetime_gmt.replace(tzinfo=timezone.utc).astimezone(tz=None)
                self.datetime_str = datetime_sgt.strftime('%Y_%m_%d_%H_%M')

            # create folder to store data
            global folder
            folder = os.path.join(self.parent_dir, self.datetime_str)
            if not os.path.isdir(folder):
                os.makedirs(folder)

            # get data from content
            jsonObj = json.loads(content) # dictonary
            data = jsonObj['value']
            return data

    def download_speedband(self):
        uri = 'http://datamall2.mytransport.sg' # resource URL
        speed_path = '/ltaodataservice/TrafficSpeedBandsv2'
        data = self.api_get_json(uri, speed_path)
        df = pd.DataFrame(data)
        df['Location'] = df['Location'].apply(lambda x: x.split(' '))
        df[['StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude']] = pd.DataFrame(df['Location'].to_list())
        filename = '{datetime}_speedband.csv'.format(datetime=self.datetime_str)
        df.to_csv(os.path.join(folder, filename), index=False)

    def download_images(self):
        uri = 'http://datamall2.mytransport.sg' # resource URL
        img_path = '/ltaodataservice/Traffic-Imagesv2'
        data = self.api_get_json(uri, img_path)
        url_link = data[0]['ImageLink']
        zipname = '_'.join(url_link.split('/')[3:5]).replace('-', '_')
        zipPath = os.path.join(folder, '%s.zip' % zipname)
        with zipfile.ZipFile(zipPath, mode='w') as img_zip:
            for i, dict in enumerate(data):
                link = dict['ImageLink']
                filename = link.split('/')[5].split('?')[0]
                url = urllib.request.urlopen(link)
                img_zip.writestr(filename, url.read())
            print(os.path.exists(zipPath))  # probing a zip file was written

    def download_incidents(self):
        uri = 'http://datamall2.mytransport.sg' # resource URL
        incident_path = '/ltaodataservice/TrafficIncidents'
        data = self.api_get_json(uri, incident_path)
        df = pd.DataFrame(data)
        filename = '{datetime}_incidents.csv'.format(datetime=self.datetime_str)
        df.to_csv(os.path.join(folder, filename), index=False)
