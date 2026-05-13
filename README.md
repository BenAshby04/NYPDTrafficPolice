# NYPD Violation Tracker

A Violation Tracker for both Drivers and system administrators


## Deployment

To deploy this project locally, run these commands in order (Assume all commands start in the root folder):

Terminal 1 (MySQL server)
```bash
  cd docker
  docker build -t nypd:1.0 .
  docker run -d -p 3306:3306 --name NYPD nypd:1.0
```
 
Terminal 2 (FastAPI)
```bash
  python -m uvicorn app.main:app --reload --port 8000
```

Terminal 3 (Web Server)
```bash
  cd Web
  python -m http.server 5500
```

Website will be available at 127.0.0.1:5500 or localhost:5500
