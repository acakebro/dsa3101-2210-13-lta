import pandas as pd
from math import radians, sqrt, sin, asin, cos

def cal_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in meters.
    r = 6.371e6
    return c * r

def closest(data, cam_coords):
    lat_long = min(data, key=lambda p: cal_distance(cam_coords["Latitude"], cam_coords["Longitude"], p["AvgLat"], p["AvgLon"]))
    index = data.index(lat_long)
    distance = cal_distance(cam_coords["Latitude"], cam_coords["Longitude"], lat_long["AvgLat"], lat_long["AvgLon"],)
    return [index, lat_long, distance]

speedband_df = pd.read_csv('./docker/speedbands.csv')
speedbands = speedband_df.iloc[:, -2:].to_dict("records")
camera_df = pd.read_csv('./docker/camera_id_lat_long.csv')

index_list = []
for camera_id in camera_df['CameraID']:
    cam_coords = (camera_df[camera_df['CameraID'] == camera_id].iloc[:, -2:].to_dict("records")[0])
    closest_speedband_index = closest(speedbands, cam_coords)[0]
    index_list.append(closest_speedband_index)
result_speedband = speedband_df.iloc[index_list]
result_speedband = result_speedband[['LinkID']]
result_speedband.reset_index(drop=True, inplace=True)
final_df = pd.concat([camera_df, result_speedband], axis=1)
print(final_df)

final_df.to_csv('./docker/closest_speedbands.csv', index=False)