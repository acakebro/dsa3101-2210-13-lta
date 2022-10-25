FROM renachongpq/dsa3101_proj_base:latest
WORKDIR /app
COPY flask_app.py flask_app.py

COPY api_calls.py api_calls.py
COPY main.py main.py
COPY vehicle_count.py vehicle_count.py
COPY vehicle_detector.py vehicle_detector.py
COPY RandomForest.py RandomForest.py
COPY ./dnn_model/yolov4.cfg ./dnn_model/yolov4.cfg
COPY ./dnn_model/yolov4.weights ./dnn_model/yolov4.weights
COPY Image_ROI.csv Image_ROI.csv
COPY camera_id_lat_long.csv camera_id_lat_long.csv
COPY closest_speedbands.csv closest_speedbands.csv
COPY training_data.csv training_data.csv
COPY model.pkl model.pkl

ENV FLASK_APP flask_app
ENTRYPOINT ["/usr/bin/python3", "/app/flask_app.py"]

