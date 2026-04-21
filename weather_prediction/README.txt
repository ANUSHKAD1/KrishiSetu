Farm Weather Dashboard

How to run (dev):
1) Create a virtualenv and install deps:
   pip install -r requirements.txt

2) Create a .env file in the project root with:
   GOOGLE_API_KEY=YOUR_GOOGLE_MAPS_API_KEY

3) Start backend:
   python app.py
   -> runs on http://127.0.0.1:5000

4) Open index.html in a Live Server (e.g., VS Code Live Server).
   The frontend calls: /api/geocode and /api/weather on port 5000.

Notes:
- Backend tries Google Weather API first (weather.googleapis.com/v1/weather:lookup).
  If it isn't enabled on your key, it falls back to Open-Meteo automatically.
- The JSON returned is normalized to what the frontend expects (dailyForecasts).

Generated: 2025-08-13T12:05:53.274629
