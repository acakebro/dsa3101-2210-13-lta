# Model and Model Diagnostics

1. Identify and obtain count of cars
2. Find ratio of grid boxes covered by vehicles to total number of grid boxes taken
   by the road (tentative)



*For object detection refer to vehicle_count.py, requires dnn_model


For main_prediction.py, after the script the response will be appended to the test_data.csv, so FE can pull data and stats from the test_data.csv to get the jam response. Additionally, FE needs to get current time when they are testing to calculate the time difference from now to when the jam started.
