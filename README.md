# Quantified Self
This is a Quantified Self API. You can create 4 different types of trackers and log them.
    The server supports exporting backup as CSV. It alerts you daily and sends a monthly report to all the registered emails. 
    Give it a try and track your life!

### Features

- 🖥️ Standalone Flask API Server
- 🌐 Single Page APP(SPA) using Vue
- 📲 Can be installed as PWA on Android or iOS
- 🔐 JWT Auth
- 🔔 Daily and monthly background alert jobs using Celery
- ⚡ Caching for fast API response using Redis
- 📄 Swagger UI Documentation for API

### Install backend requirements
```
cd /Backend
pip install -r requirements.txt

```

### Install frontend requirements
```
cd /Frontend
npm install
```
<br>

## Project setup
<br>

### Run API server 
```
cd /Backend
python3 main.py
```


### Run Redis server 
```
redis-server
```

### Run celery tasks and beat scheduler
```
celery -A tasks worker -l INFO
celery -A tasks beat
```


## Frontend Server

### Compiles and hot-reloads for development
```
npm run serve
```

### Compile for building PWA
```
npm run build
```
### Deploy dist folder
```
cd  /dist
python3 -m http.server
```