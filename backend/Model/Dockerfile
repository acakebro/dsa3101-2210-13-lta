FROM python:3.10.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
COPY flask_app.py flask_app.py

COPY api_calls.py api_calls.py
COPY main.py main.py
COPY vehicle_count.py vehicle_count.py
COPY vehicle_detector.py vehicle_detector.py
COPY RandomForest.py RandomForest.py
COPY yolov4.cfg yolov4.cfg
COPY yolov4.weights yolov4.weights
COPY Image_ROI.csv Image_ROI.csv
COPY camera_id_lat_long.csv camera_id_lat_long.csv
COPY closest_speedbands.csv closest_speedbands.csv
COPY training_data.csv training_data.csv

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ENV FLASK_APP flask_app.py

ENTRYPOINT [ "python", "-u", "-m", "flask", "run", "--host=0.0.0.0"]
 
