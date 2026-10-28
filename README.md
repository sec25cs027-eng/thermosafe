# ThermoSafe

Hyperlocal heat-stress alerts and work-rest plans for outdoor workers in India.

## Problem
Outdoor workers (construction, farming, delivery, vending) face dangerous heat but only get district-level temperature from weather apps. There is no humidity-adjusted, job-specific guidance.

## Solution
ThermoSafe takes a location and job type, fetches live weather from Open-Meteo, computes a heat index, adjusts it for how physically heavy the job is, and returns a risk level with a work-rest-hydration plan.

## Features
- Live weather via Open-Meteo (free, no API key)
- Heat index using the NWS Rothfusz formula
- Job-based risk adjustment (heavy / moderate / light work)
- Risk levels: Low, Caution, High, Danger, Extreme, each with advice
- Unit tests and sample data included

## Roadmap
Telegram/WhatsApp/SMS alerts in Tamil, Hindi and English, and an employer site-risk dashboard.

## Setup
```bash
git clone https://github.com/<your-username>/thermosafe.git
cd thermosafe
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Environment variables
None are required for the current prototype (Open-Meteo needs no key).
Planned for the messaging bot: `TELEGRAM_BOT_TOKEN`.

## Usage
Open http://127.0.0.1:8000/docs, or call:

```
GET /risk?lat=13.08&lon=80.27&job=construction
```

Example response:
```json
{
  "temperature_c": 34.1,
  "humidity_pct": 68,
  "heat_index_c": 46.2,
  "adjusted_index_c": 49.2,
  "job": "construction",
  "risk_level": "Danger",
  "advice": "Rest 15-20 min every hour. Avoid 12-3 PM work. Watch for dizziness."
}
```

## Tests
```bash
pytest
```

## Documentation
See [docs/design.md](docs/design.md) for the architecture.

## License
MIT
