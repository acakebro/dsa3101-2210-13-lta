import json
import requests
import urllib
from urllib.parse import urlparse
import httplib2 as http  # external library
#pip install httplib2
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

def geospatial_layers_link2folder(data, parent_dir):
    layers_path = os.path.join(parent_dir,"layers/") 
    if not os.path.isdir(layers_path):
        # Create the directory images
        os.mkdir(layers_path) 
    #else download in layers
    os.chdir(layers_path)
    link = data['value'][0]['Link']
    resource = urllib.request.urlopen(link)
    startindex = len("https://dmgeospatial.s3.ap-southeast-1.amazonaws.com/")
    endindex = link.find(".zip") + len(".zip")
    name = link[startindex:endindex]
    print("Downloading", name)
    output = open(name, "wb")
    output.write(resource.read())
    output.close()
    os.chdir(parent_dir)
    

def download_geospatial_layers(parentdir, layers):
    uri = "http://datamall2.mytransport.sg/ltaodataservice/GeospatialWholeIsland"
    jsonfilename = "temporary_geospatial_layer.json"
    jsonfiledir = os.path.join(parentdir, jsonfilename) 
    print("Updating", jsonfilename)
    for layer in layers:
        finaluri = uri+"?ID="+layer
        os.chdir(parentdir)
        updatejson(finaluri,jsonfilename) #overwrites
        geospatial_layers_link2folder(loadjson(jsonfiledir), parentdir)


'''
import fiona

shape = fiona.open("ArrowMarking.shp")
print(shape.schema)
{'geometry': 'LineString', 'properties': OrderedDict([(u'FID', 'float:11')])}
#first feature of the shapefile
first = shape.next()
print(first) # (GeoJSON format)
{'geometry': {'type': 'LineString', 'coordinates': [(0.0, 0.0), (25.0, 10.0), (50.0, 50.0)]}, 'type': 'Feature', 'id': '0', 'properties': OrderedDict([(u'FID', 0.0)])}
'''

