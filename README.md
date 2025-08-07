# Youtube Fetch Api

# Project Goal

To make an API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

# Basic Requirements:

- Server should call the YouTube API continuously in background (async) with some interval (say 10 seconds) for fetching the latest videos for a predefined search query and should store the data of videos (specifically these fields - Video title, description, publishing datetime, thumbnails URLs and any other fields you require) in a database with proper indexes.
- A GET API which returns the stored video data in a paginated response sorted in descending order of published datetime.
- It should be scalable and optimised.

# Bonus Points:

- Add support for supplying multiple API keys so that if quota is exhausted on one, it automatically uses the next available key.
- Make a dashboard to view the stored videos with filters and sorting options (optional)

## Build Instructions
### Simple installation
The command below, build the complete application using docker-compose
* Redis
* MySQL
* Celery Worker
* Celery Beat
* FastAPI web application
```
docker-compose up
```
## Build applictions individually
In order to build applications individually, the repootory comes with stand-alone Dockerfiles and theor corresponding docker-compose files. Follow the commands to build the application individually.
### To trigger the periodic Youtube API ping
```
cd app
```
```
docker-compose up
```
### To start the web-server running on FAST API to connect to the mysql db
```
cd web-server
```
```
docker-compose up
```
### No DockerCompose Installation
MySQL DB for holding data
```
docker run -e MYSQL_ROOT_PASSWORD=my-secret-pw -p 3306:3306 mysql
```
Redis for broker and backend to Celery
```
docker run -it --rm --name redis --net redis -p 6379:6379 redis:6.0-alpine
```
```
cd app
```
Initiate the Celery workers and Beat.
```
celery -A worker.celery_worker worker -l info
```
```
celery -A worker.celery_worker beat -l info
```
```
cd ../web-server
```
Run the web server.
```
uvicorn main:app --reload
```

### Project

# Tech Stack

<p align="left">
        <a href="https://www.docker.com/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a>
        <a href="https://www.elastic.co" target="_blank"> <img src="https://www.vectorlogo.zone/logos/elastic/elastic-icon.svg" alt="elasticsearch" width="40" height="40"/> </a>
        <a href="https://expressjs.com" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/express/express-original-wordmark.svg" alt="express" width="40" height="40"/> </a>
        <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="javascript" width="40" height="40"/> </a>
        <a href="https://www.nginx.com" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nginx/nginx-original.svg" alt="nginx" width="40" height="40"/> </a>
        <a href="https://nodejs.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nodejs/nodejs-original-wordmark.svg" alt="nodejs" width="40" height="40"/> </a>
</p>

# Reference:

- YouTube data v3 API: [https://developers.google.com/youtube/v3/getting-started](https://developers.google.com/youtube/v3/getting-started)
- Search API reference: [https://developers.google.com/youtube/v3/docs/search/list](https://developers.google.com/youtube/v3/docs/search/list)
