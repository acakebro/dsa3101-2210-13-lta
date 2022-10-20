import json
from pickle import TRUE
import requests
import urllib
from urllib.parse import urlparse
import httplib2 as http  # external library
import csv
import os
import time
import pandas as pd
import cv2
import glob  # allows us to load all the path of all the files in a folder
from vehicle_detector import VehicleDetector
import ast
import numpy as np

# change to desired dir
#get directory
parent_dir = ("/Users/rebecca/dummy/")
os.chdir(parent_dir)
image_roi_df = pd.read_csv(parent_dir + 'Image_ROI.csv') #has Camera_Id, ROI and Direction
cam_df = pd.read_csv(parent_dir + 'Cam_Locations.csv') #has Camera_Id, Latitude and Longitude
link_df =pd.read_csv(parent_dir + 'Link_Locations.csv') #has 'LinkID','RoadCategory','RoadName','lat1','lng1','lat2','lng2'
  # camID, linkid, dist (more accurate -> def #camID, roi/direction, weight/dist, linkID )

# Load Vehicle Detector
vd = VehicleDetector()  # instantiate the instance

def updatejson(uri,tempjson): #overwrites tempjson, gets json of either images or speedbands
    headers = {"AccountKey": "AO4qMbK3S7CWKSlplQZqlA==", "accept": "application/json"}

    #Save result to file
    target = urlparse(uri)
    method = "GET"
    body = ""

    h=http.Http() 
    response, content = h.request(uri, method, body, headers)
    jsonObj = json.loads(content)

    #updatejson, overwrites tempjson
    with open(tempjson,"w") as outfile: #write in json file
    #Saving jsonObj["d"]
       json.dump(jsonObj, outfile, sort_keys=True, indent=4, ensure_ascii=False)
    print("Updated", tempjson)

    jsonfiledir = os.path.join(parent_dir, tempjson) 
    with open(jsonfiledir) as json_file: #eg. '/Users/rebecca/Y3S1/DSA3101/tempory.json'
        jsonObj = json.load(json_file)
    return jsonObj

def roi(img, coords):
    x = int(img.shape[1])
    y = int(img.shape[0])
    if len(coords) < 4:
        print('minimum 4 coordinates required')
        return
    shape = np.array(coords)  # shape of roi
    mask = np.zeros_like(img)  # np array with zeros (of image dimension)

    # creates a polygon with the mask colour (blue), areas not in roi would be black (pixel is 0)
    cv2.fillPoly(mask, pts=np.int32([shape]), color=(255, 255, 255))

    # select ares where mask pixels are not zero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def images_df():
    uri = "http://datamall2.mytransport.sg/ltaodataservice/Traffic-Imagesv2"
    jsonfilename = "temporary_traffic_images.json"
    jsonObj = updatejson(uri ,jsonfilename)
    data = jsonObj['value']
    df = pd.DataFrame(data)

    #get ImageLink
    link = df['ImageLink']
    
    #get Images
    print('Getting Images...')
    resource = link.apply(lambda x: urllib.request.urlopen(x))
    df['Imgs'] = resource.apply(lambda x: np.asarray(bytearray(x.read()), dtype="uint8"))
    df['Imgs'] = df['Imgs'].apply(lambda x: cv2.imdecode(x, cv2.IMREAD_COLOR))    
    #df['Imgs'] = resource.apply(lambda x: x.read())
    #df['Imgs'] = resource.apply(lambda x: cv2.imread(x))

    #get Timestamp
    index = len("https://dm-traffic-camera-itsc.s3.ap-southeast-1.amazonaws.com/2022-10-08/08-50/1001_0843_")
    time = link.apply(lambda x: x[index:index+len("20221008085001")])
    df['Timestamp'] = time
    print('Timestamp column added')

    #replace ImageLink with img filename
    df.rename({'ImageLink': 'FileName'}, axis=1, inplace=True)

    #replace ImageLink values with img filename
    index = len("https://dm-traffic-camera-itsc.s3.ap-southeast-1.amazonaws.com/2022-10-08/08-50/")
    name = link.apply(lambda x: x[index:index+len("1001_0843_20221008085001_525510.jpg")])
    df['FileName'] = name

    #getting Weighted Speed 
    temp_df = dist_df[ dist_df['CameraID'] == '1001']
    smallestvalue = temp_df.nsmallest(1, 'Dist')['Dist']
    print(smallestvalue)
    radius = smallestvalue
    if smallestvalue < 100:
        radius += 100
    elif smallestvalue < 500:
        radius += 200

    #add Speed
    speed = ['888']* len(df)
    df['Speed'] = speed
    print('Speed column added')

    #add ROI direction
    image_roi_df['Camera_Id']=image_roi_df['Camera_Id'].astype(str) #change to str #no meaning as int type
    df = df.merge(image_roi_df, left_on ='CameraID',right_on ='Camera_Id').drop("Camera_Id", 1)

    #add CarCount
    count = []
    for i in df.index: #maybe can filter some so dh to run all (if cam_id == '1001', run else continue)
        camera = df['CameraID'][i]
        direction = df['Direction'][i] #just to see
        label = camera + " " + direction #just to see
        if camera == '1001' or camera == '1002' : # to narrow down 
            print("Counting... ",(i+1),"/ 191") #len(df) = 191
            roi_coords = ast.literal_eval(df['ROI'][i])
            #direction = df['Direction'][i]
            img = df['Imgs'][i]
            roi_img = roi(img, roi_coords)
            vehicle_boxes = vd.detect_vehicles(roi_img)
            vehicle_count = len(vehicle_boxes)
            count.append(vehicle_count)
            #just to see, no boxes
            cv2.imshow("LTA " + label, roi_img) 
            cv2.waitKey() #press any key to go to next img
            cv2.destroyAllWindows()
        else:
            count.append(999)
        
        #length = length_df[i]
        #density = count/length
        
    df['CarCount'] = count

    # remove ROI col
    df.drop('ROI', 1, inplace = True) 

    #calc length 
    length = ['777']* len(df)
    df['RoadLength'] = length

    #add Density
    density = ['666']* len(df) # calc using count & length
    df['Density'] = density

    return df


def speedband_df():
    uri = "http://datamall2.mytransport.sg/ltaodataservice/TrafficSpeedBandsv2"
    jsonfilename = "temporary_traffic_speedbands.json"
    jsonObj = updatejson(uri ,jsonfilename)
    data = jsonObj['value']
    df = pd.DataFrame(data)[['LinkID','Location','RoadCategory','RoadName','SpeedBand']]

    # add ExtractedTime
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    df['ExtractedTime'] = [time_string]*len(df)

    #split Location into lat1,lng1,lat2,lng2
    df['lat1'] = df['Location'].apply(lambda x: x.split(' ')[0])
    df['lng1'] = df['Location'].apply(lambda x: x.split(' ')[1])
    df['lat2'] = df['Location'].apply(lambda x: x.split(' ')[2])
    df['lng2'] = df['Location'].apply(lambda x: x.split(' ')[3])
    df.drop("Location", 1, inplace=True)

    #ave speed
    df['SpeedBand'] = df['SpeedBand'].apply(lambda x: x*10-5) #ave speed = middle value of speedband
    df.rename({'SpeedBand': 'AveSpeed'}, axis=1, inplace=True)
    
    return df

#update distances

def curr_distances():
    #cam_df
    #link_df  #dist roughly the same aka weight #speedband coords the same #speed diff (combine in w linkid as )
    distance_col =[]
    camera_col =[]
    link_col =[]
    for cam_ind in cam_df.index:
        cam_lat = cam_df['Latitude'][cam_ind]
        cam_lng = cam_df['Longitude'][cam_ind]
        cam_id = cam_df['CameraID'][cam_ind]
        for band_ind in link_df.index:
            print(str(cam_ind) + str(band_ind)) #can add a check to skip when radius dist is > 10km?
            distto1 = get_dist(cam_lat,cam_lng,link_df['lat1'][band_ind],link_df['lng1'][band_ind])
            distto2 = get_dist(cam_lat,cam_lng,link_df['lat2'][band_ind],link_df['lng2'][band_ind])
            dist = min(distto1,distto2)
            linkid = link_df['LinkID'][band_ind]
            distance_col.append(dist)
            camera_col.append(cam_id)
            link_col.append(linkid)
    dist_df = pd.DataFrame(list(zip(distance_col, camera_col, link_col)),
               columns =['Dist', 'CameraID','LinkID'])
    dist_df.to_csv('Estimated_Distances.csv') #camID, dist, linkID 
    #return dist_df #to csv because it is too much to load

def get_dist(latcoord_ori,lngcoord_ori,latcoord_des,lngcoord_des): #in cm
    api = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="
    lat_ori = str(latcoord_ori) + "%2C" #%2C rep comma
    lng_ori = str(lngcoord_ori) + "&destinations="
    lat_des = str(latcoord_des) + "%2C"
    lng_des = str(lngcoord_des) + "&key=TYPETHEAPIKEYHERE" #dm rebecca for API key
    url = api + lat_ori + lng_ori + lat_des+ lng_des
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    dist_value = list(response.text.split("distance"))[1].split("value")[1].split(":")[1].split("}")[0].strip()
    return dist_value

curr_distances() #only run once to make Estimated_Distances.csv

#distances from cam to incidents
#get coordinate

#################
def make_cam_df(): 
    uri = "http://datamall2.mytransport.sg/ltaodataservice/Traffic-Imagesv2"
    jsonfilename = "temporary_traffic_images.json"
    jsonObj = updatejson(uri ,jsonfilename)
    data = jsonObj['value']
    df = pd.DataFrame(data)
    cam_df = df[['CameraID', 'Latitude', 'Longitude']] #could be from any images dataset 
    cam_df.to_csv('Cam_Locations.csv')

#make_cam_df() #only run once to make Cam_Locations.csv

def make_link_df(): 
    uri = "http://datamall2.mytransport.sg/ltaodataservice/TrafficSpeedBandsv2"
    jsonfilename = "temporary_traffic_speedbands.json"
    jsonObj = updatejson(uri ,jsonfilename)
    data = jsonObj['value']
    link_df = pd.DataFrame(data)[['LinkID','Location','RoadCategory','RoadName']] #could be from any speedband dataset 
    #split Location into lat1,lng1,lat2,lng2
    link_df['lat1'] = link_df['Location'].apply(lambda x: x.split(' ')[0])
    link_df['lng1'] = link_df['Location'].apply(lambda x: x.split(' ')[1])
    link_df['lat2'] = link_df['Location'].apply(lambda x: x.split(' ')[2])
    link_df['lng2'] = link_df['Location'].apply(lambda x: x.split(' ')[3])
    link_df.drop("Location", 1, inplace=True)
    link_df.to_csv('Link_Locations.csv') 

#make_link_df() #only run once to make Link_Locations.csv
################

#images_df()
#print(images_df())
#print(speedband_df())