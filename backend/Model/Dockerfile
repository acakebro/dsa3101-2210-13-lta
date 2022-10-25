FROM python:3.10.8-slim-buster
WORKDIR /app
COPY . .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ENV FLASK_APP flask_app.py

ENTRYPOINT [ "python", "-u", "-m", "flask", "run", "--host=0.0.0.0"]
 
