# Model and Model Diagnostics

1. Identify and obtain count of cars
2. Find ratio of grid boxes covered by vehicles to total number of grid boxes taken
   by the road (tentative)



*For object detection refer to vehicle_count.py, requires dnn_model


For main_prediction.py, after the script the response will be appended to the test_data.csv, so FE can pull data and stats from the test_data.csv to get the jam response. Additionally, FE needs to get current time when they are testing to calculate the time difference from now to when the jam started.

(as of 21 Oct) </br>
`main.py` </br>
-> run requires `vehicle_count.py`, `api_calls.py`, `vehicle_detector.py`, `dnn_model` folder, `ROI` folder, `camera_id_lat_long.csv` </br>
-> will create csvs and a folder 'api_data' to store them </br>
-> output is a df with "Camera_Id", 
                "Direction", 
                "Vehicle_Count",
                "Density",
                "Average_Speed",
                "Date",
                "Time",
                "Latitude",
                "Longitude",
                "Is_Weekday",
                "Is_Peak" </br>
</br>
`vehicle_count.py` </br>
->  class for car counting </br>
</br>
`api_calls.py` </br>
->  just the class </br>
