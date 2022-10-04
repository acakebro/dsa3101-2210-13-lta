import json
import requests
import urllib
import os

from urllib.parse import urlparse

import httplib2 as http  # external library
from PIL import Image
from io import BytesIO


if __name__ == "__main__":

    headers = {"AccountKey": "AO4qMbK3S7CWKSlplQZqlA==", "accept": "application/json"}
    # API parameters
    uri = "http://datamall2.mytransport.sg/ltaodataservice/Traffic-Imagesv2?skip=1000"
    # Build query string & specify type
    target = urlparse(uri)
    print(target.geturl())
    method = "GET"
    body = ""
    h = http.Http()
    response, content = h.request(uri, method, body, headers)

    # Parse JSON to print
    jsonObj = json.loads(content)
    # print json.dumps(jsonObj, sort_keys=True, indent=4)
    print(os.getcwd())

    # creating a json file to populate
    with open("trafficImages.json", "w") as outfile:
        json.dump(jsonObj, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    data = jsonObj["value"]  # this will be a list
    path = (
        "/Users/calebchia/Documents/NUS/Y3S1/DSA3101/Project/dsa3101-2210-13-lta/images"
    )

    # Loading the images to a specific folder
    os.chdir(path)  # so that images are stored in that specific folder
    print("Loading images...")
    for cam in data:  # cam will be dict
        id_ = cam["CameraID"]
        link = cam["ImageLink"]
        index = link.find("X-Amz-Date=") + len("X-Amz-Date=")
        time = link[index : index + len("20220921T034020")]
        resource = urllib.request.urlopen(link)
        name = id_ + "_" + time
        output = open(name + ".jpg", "wb")
        output.write(resource.read())
        output.close()
    # resetting the path directory
    print("Images fully loaded")
    newpath = "/Users/calebchia/Documents/NUS/Y3S1/DSA3101/Project/dsa3101-2210-13-lta"
    os.chdir(newpath)
