
# NYPD Violation Tracker

A Violation Tracker for both Drivers and system administrators


## Installation

Clone the Repository

```bash
git clone https://github.com/BenAshby04/NYPDTrafficPolice.git
cd NYPDTrafficPolice
```
    
## Deployment

To deploy this project locally, run these commands in order (Assume all commands start in the root folder):

Terminal 1 (MySQL server)
```bash
  cd docker
  docker build -t nypd:1.0
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
## Troubleshooting

### "Could not connect to MySQL"
- Verify MySQL is running.
- Check the credentials in `app/db/session.py` match your local MySQL setup.
- Make sure the `NYPD` database exists.

### "CORS error" in the browser console
- Confirm the FastAPI backend is running on port 8000.
- The allowed origins in `app/main.py` include `http://127.0.0.1:5500` and `http://localhost:5500`. If you're serving the frontend on a different port, add it to the `allow_origins` list.

### Admin login says "Access denied"
- The user being logged in does not have `UserRole = 'admin'`. Use the default `root` account, or set a user's `UserRole` to `admin` directly in MySQL.

### Driver dashboard shows "No violations on record"
- This may be correct — the driver genuinely has no citations.
- Verify by querying directly: `CALL NYPD.GetCiviData('THEIR_DL_NUMBER');` in MySQL Workbench.
- If you see rows with non-null `NID` values but the dashboard still shows nothing, check the browser console for JavaScript errors.


## Authors

- [@BenAshby04](https://github.com/BenAshby04/) -  Ben Ashby (29007019)


## License

Submitted as coursework for CMP2812 at the University of Lincoln. Not licensed for redistribution.
