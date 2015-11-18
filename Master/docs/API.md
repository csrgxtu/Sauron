## Sauron Master API V1.0

### 1, UnvisitedUrls CRUD Operations
#### *Read* urls from UnvisitedUrls
```bash
GET http://localhost:5000/unvisitedurls?start=0&offset=10&spider=google
```
#### *Retrieve* urls from UnvisitedUrls
```bash
POST http://localhost:5000/unvisitedurls?start=0&offset=10&spider=google
```
#### *Insert* urls into UnvisitedUrls
```bash
PUT http://localhost:5000/unvisitedurls

Json body = {'urls': [{'url': 'http://google.com', 'spider': 'google'}]}
```
Example
```bash
curl -X PUT -H 'Content-Type: application/json' -d '{"urls": [{"url": "http://google.com", "spider": "google"}]}' http://localhost:5000/unvisitedurls
```
#### *Delete* urls from UnvisitedUrls
```bash
DELETE http://localhost:5000/unvisitedurls

Json body = {'ids': ['id', 'id']}
```
Example
```
curl -X DELETE -H 'Content-Type: application/json' -d '{"ids": ["ids", "ids"]}' http://localhost:5000/unvisitedurls
```

### 2, VisitedUrls CRUD Operations
#### *Read* urls from VisitedUrls
```bash
GET http://localhost:5000/visitedurls?start=0&offset=10&spider=google
```
#### *Retrieve* urls from VisitedUrls
```bash
POST http://localhost:5000/visitedurls?start=0&offset=10&spider=google
```
#### *Insert* urls into VisitedUrls
```bash
PUT http://localhost:5000/visitedurls

Json body = {'urls': [{'url': 'http://google.com', 'spider': 'google'}]}
```
Example
```bash
curl -X PUT -H 'Content-Type: application/json' -d '{"urls": [{"url": "http://google.com", "spider": "google"}]}' http://localhost:5000/visitedurls
```
#### *Delete* urls from VisitedUrls
```bash
DELETE http://localhost:5000/visitedurls

Json body = {'ids': ['id', 'id']}
```
Example
```
curl -X DELETE -H 'Content-Type: application/json' -d '{"ids": ["ids", "ids"]}' http://localhost:5000/visitedurls
```

### 3, DeadUrls CRUD Operations
#### *Read* urls from DeadUrls
```bash
GET http://localhost:5000/deadurls?start=0&offset=10&spider=google
```
#### *Retrieve* urls from DeadUrls
```bash
POST http://localhost:5000/deadurls?start=0&offset=10&spider=google
```
#### *Insert* urls into DeadUrls
```bash
PUT http://localhost:5000/deadurls

Json body = {'urls': [{'url': 'http://google.com', 'spider': 'google'}]}
```
Example
```bash
curl -X PUT -H 'Content-Type: application/json' -d '{"urls": [{"url": "http://google.com", "spider": "google"}]}' http://localhost:5000/deadurls
```
#### *Delete* urls from DeadUrls
```bash
DELETE http://localhost:5000/deadurls

Json body = {'ids': ['id', 'id']}
```
Example
```
curl -X DELETE -H 'Content-Type: application/json' -d '{"ids": ["ids", "ids"]}' http://localhost:5000/deadurls
```

### 4, Data CRUD Operation
#### *Read* datas from Data
```bash
GET http://localhost:5000/data?start=0&offset=10&spider=google
```
#### *Retrieve* data from Data
```bash
POST http://localhost:5000/data?start=0&offset=10&spider=google
```
#### *Insert* data into Data
```bash
PUT http://localhost:5000/data

# Json body = {'datas': [{'url': 'http://google.com', 'data': 'blabla', 'spider': 'google'}]}
```
Example
```bash
curl -X PUT -H 'Content-Type: application/json' -d '{"datas": [{"url": "http://google.com", "data": "blabla", "spider": "google"}]}' http://localhost:5000/data
```
#### *Delete* data from Data
```bash
DELETE http://localhost:5000/data

Json body = {'ids': ['id', 'id']}
```
Example
```
curl -X DELETE -H 'Content-Type: application/json' -d '{"ids": ["ids", "ids"]}' http://localhost:5000/data
```

### 4, File CRUD Operation
#### *Read* files from file
```bash
GET http://localhost:5000/file?start=0&offset=10&spider=google
```
#### *Retrieve* file from File
```bash
POST http://localhost:5000/file?start=0&offset=10&spider=google
```
#### *Insert* file into File
```bash
PUT http://localhost:5000/file

Json body = {'files': [{"url": "http://google.com", "head": "http head", "body": "html", "spider": "google"}]}
```
Example
```bash
curl -X PUT -H 'Content-Type: application/json' -d '{"files": [{"url": "http://google.com", "head": "http head", "body": "html", "spider": "google"}]}' http://localhost:5000/file
```
#### *Delete* file from File
```bash
DELETE http://localhost:5000/file

Json body = {'ids': ['id', 'id']}
```
Example
```
curl -X DELETE -H 'Content-Type: application/json' -d '{"ids": ["ids", "ids"]}' http://localhost:5000/file
```
