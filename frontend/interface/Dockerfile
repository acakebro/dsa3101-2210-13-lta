FROM python:3.10.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
COPY flask_app.py flask_app.py

COPY index.py index.py
COPY pg1.py pg1.py
COPY pg2.py pg2.py
COPY pg3.py pg3.py
COPY app.py app.py
COPY train_data.csv train_data.csv

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ENV FLASK_APP flask_app.py
RUN python3 index.py

ENTRYPOINT [ "python", "-u", "-m", "flask", "run", "--host=0.0.0.0"]
 
