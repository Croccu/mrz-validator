# MRZ Validator

A minimal tool to validate passport MRZ (Machine Readable Zone) strings based on ICAO 9303 TD3 format. The app verifies all official check digits and provides instant feedback.

NB! Please note that this is currently only for passport MRZ validation, not ID's etc.

## Features

- Input validation and padding to 44 characters
- Verifies:
  - Passport number check digit
  - Date of birth check digit
  - Expiry date check digit
  - Final line check digit
- Simple React frontend
- Flask API backend with rate limiting via Redis
- Deployed on Heroku
- CORS-restricted to allow safe API access

## Stack

- **Frontend:** React (with basic JSX, no extra libraries)
- **Backend:** Flask (Python), with Flask-Limiter and flask-cors
- **Rate Limiting:** Redis (via Heroku add-on)
- **Deployment:** Heroku

## Project Structure

```
MRZ_VALIDATOR/
├── backend/
│   ├── app.py
│   ├── mrz_validator.py
│   ├── requirements.txt
│   └── Procfile
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── ...
```

## Setup & Running Locally

### Backend (Python API)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Frontend (React)

```bash
cd frontend
npm install
npm start
```

To build for production:

```bash
npm run build
```

This generates the React static files inside `frontend/build`, which the Flask app serves when deployed.

## Deployment (Heroku)

1. Set up Redis add-on on Heroku:

```bash
heroku addons:create heroku-redis:hobby-dev
```

2. Push backend to Heroku:

```bash
cd backend
git push heroku master
```

3. Make sure frontend is built and served via Flask static folder.

## Notes

- The rate limiter defaults to 6 validation requests per minute per IP.
- Redis SSL verification is turned off due to Heroku’s certificate chain behavior.
- The MRZ check digit logic strictly follows ICAO 9303 rules (modulus 10 with character weighting).
- This app is intended for internal use, prototyping, and testing purposes.
