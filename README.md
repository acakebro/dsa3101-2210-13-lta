# dsa3101-2210-13-lta

LTA Modelling by group 13
````
├── backend 
│   ├── Exploratory Scripts 
│   │   └──  API-Exploration - making api calls and understanding the data we have 
│   │   └──  Dummy - combining the functions using dummy values to output a data frame 
│   │   └──  Image-Processing-Related - other ways we tried to process the image 
│   ├── Image-Processing - final scripts we used to get data from images and their saved outputs 
│   └── Model - finalised scripts that we containerise 
├── frontend 
│   ├── interface -all files that we containerise 
│   ├── src - individual work with sample data to do local testing
│   ├── Procfile 
│   └── runtime.txt 
├── .gitattributes 
├── .gitignore 
└── docker-compose.yml 
````
````
How to use the code and deploy the interface?
1. git clone git@github.com:acakebro/dsa3101-2210-13-lta.git
2. open docker desktop
3. In shell:
   cd dsa3101-2210-13-lta
   docker compose up
4. go to docker desktop, click on open backend container in browser
5. wait for around 15 mins for the file traffic_stats.csv to appear in /app and incidents.csv to appear in /app/assets
6. check it by doing ls in the docker terminal
7. after traffic_stats.csv appears in the backend container directory
8. open frontend in browser

Take note that every run of the container, you need to remove frontend and backend images for data to be up to date.
````

