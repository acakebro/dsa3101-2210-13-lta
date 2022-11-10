FROM python:3.10.8-slim-buster
WORKDIR /app

#copy all files from directory
COPY . .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 8050

CMD ["python", "index.py"]