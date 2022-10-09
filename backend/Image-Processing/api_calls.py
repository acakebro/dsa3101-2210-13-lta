import json
import requests
import urllib
from urllib.parse import urlparse
import httplib2 as http  # external library
#pip install httplib2
import csv
import os
import time
import pandas as pd

def updatejson(uri,tempjson): #overwrites tempjson
    headers = {"AccountKey": "AO4qMbK3S7CWKSlplQZqlA==", "accept": "application/json"}

    #Save result to file
    target = urlparse(uri)
    method = "GET"
    body = ""

    h=http.Http() 
    response, content = h.request(uri, method, body, headers)
    jsonObj = json.loads(content)

    with open(tempjson,"w") as outfile: #write in json file
    #Saving jsonObj["d"]
       json.dump(jsonObj, outfile, sort_keys=True, indent=4, ensure_ascii=False)
    print("Updated", tempjson)
    return outfile

def loadjson(filedir): #eg. '/Users/rebecca/Y3S1/DSA3101/response.json'
    with open(filedir) as json_file:
        data = json.load(json_file)
    return (data)

def get_data(uri, jsonfilename, jsonfiledir, csvfilename, json2csv):
    if os.path.exists(csvfilename) == False: # set up
        header = "yes"
    else: #append
        header = "no"
    file_path = open(csvfilename, 'a')
    a = csv.writer(file_path)
    updatejson(uri,jsonfilename) #overwrites
    json2csv(loadjson(jsonfiledir), a, header)
    print("Updated", csvfilename)
    file_path.close()

def traffic_images_json2csv(data, path, header):
    for i,dict in enumerate(data['value']):
        if (header == "yes" and i == 0):
            header = list(dict.keys())
            header.append('Timestamp')
            path.writerow(header)

        row = list(dict.values())
        link = dict['ImageLink']
        index = len("https://dm-traffic-camera-itsc.s3.ap-southeast-1.amazonaws.com/2022-10-08/08-50/1001_0843_")
        time = link[index:index+len("20221008085001")]
        row.append(time)
        path.writerow(row)

def traffic_images_link2folder(data, parent_dir):
    images_path = os.path.join(parent_dir,"images/") 
    if not os.path.isdir(images_path):
        # Create the directory images
        os.mkdir(images_path) 
        os.chdir(images_path)
    link = data['value'][0]['ImageLink']
    index = len("https://dm-traffic-camera-itsc.s3.ap-southeast-1.amazonaws.com/")
    directory = link[index:index+len("2022-10-08/08-50")].replace("/","_").replace("-","_")
    path = os.path.join(images_path, directory) 
    if not os.path.isdir(path):
        # Create the directory for each folder
        os.mkdir(path) 
        os.chdir(path)
        print("Loading images...")
        for cam in data['value']:
            link = cam["ImageLink"]
            resource = urllib.request.urlopen(link)
            index = len("https://dm-traffic-camera-itsc.s3.ap-southeast-1.amazonaws.com/2022-10-08/08-50/")
            name = link[index:index+len("1001_0843_20221008085001_525510.jpg")]
            output = open(name, "wb")
            output.write(resource.read())
            output.close()
        os.chdir(parent_dir)
    #else don't download (downloaded before)
    

def traffic_incidents_json2csv(data, path, header):
    for i,dict in enumerate(data['value']):
        if (header == "yes" and i == 0):
            header = list(dict.keys())
            #header.append('Timestamp')
            path.writerow(header)
        row = list(dict.values())
        path.writerow(row)

def traffic_speedbands_json2csv(data, path, header):
    for i,dict in enumerate(data['value']):
        if (header == "yes" and i == 0):
            header = list(dict.keys())
            header.append('Extract Time')
            path.writerow(header)
        row = list(dict.values())
        named_tuple = time.localtime() # get struct_time
        time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
        row.append(time_string)
        path.writerow(row)

# change to desired dir
parent_dir = ("/Users/rebecca/")
os.chdir(parent_dir)

#traffic images
uri = "http://datamall2.mytransport.sg/ltaodataservice/Traffic-Imagesv2"
jsonfilename = "temporary_traffic_images.json"
jsonfiledir = os.path.join(parent_dir, jsonfilename) 
csvfilename = 'traffic_images.csv'
get_data(uri, jsonfilename,jsonfiledir , csvfilename, traffic_images_json2csv)
traffic_images_link2folder(loadjson(jsonfiledir), parent_dir)

#traffic incidents
uri = "http://datamall2.mytransport.sg/ltaodataservice/TrafficIncidents"
jsonfilename = "temporary_traffic_incidents.json"
jsonfiledir = os.path.join(parent_dir, jsonfilename) 
csvfilename = 'traffic_incidents.csv'
get_data(uri, jsonfilename, jsonfiledir, csvfilename, traffic_incidents_json2csv) 

#traffic speedbands
uri = "http://datamall2.mytransport.sg/ltaodataservice/TrafficSpeedBandsv2"
jsonfilename = "temporary_traffic_speedbands.json"
jsonfiledir = os.path.join(parent_dir, jsonfilename) 
csvfilename = 'traffic_speedbands.csv'
get_data(uri, jsonfilename, jsonfiledir, csvfilename, traffic_speedbands_json2csv) 


#run exit() if you face a 'syntax error'
def rm_dup(file_name, file_name_output, keys):
    df = pd.read_csv(file_name)
    # Notes:
    # - the `subset=None` means that every column is used 
    #    to determine if two rows are different; to change that specify
    #    the columns as an array
    # - the `inplace=True` means that the data structure is changed and
    #   the duplicate rows are gone  
    df.drop_duplicates(subset=keys, inplace=True)
    # Write the results to a different file
    df.to_csv(file_name_output, index=False) #sep =';' puts it in cols
    print("Updated", file_name_output)

file_name = 'traffic_incidents.csv'
file_name_output = 'traffic_incidents_no_dup.csv'
incident_keys = None
rm_dup(file_name, file_name_output,incident_keys)

file_name = 'traffic_speedbands.csv'
file_name_output = 'traffic_speedbands_no_dup.csv'
speedband_keys = None
rm_dup(file_name, file_name_output,speedband_keys)

file_name = 'traffic_images.csv'
file_name_output = 'traffic_images_no_dup.csv'
images_keys = ['CameraID', 'Timestamp'] #None also can, 'CameraID', 'Timestamp' 
rm_dup(file_name, file_name_output,images_keys)