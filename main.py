"""ThermoSafe - heat-stress risk API for outdoor workers."""
import requests
from fastapi import FastAPI, HTTPException

app = FastAPI(title="ThermoSafe", version="0.1.0")

OPEN_METEO = "https://api.open-meteo.com/v1/forecast"

HEAVY = {"construction", "farming", "loader", "mason"}
MODERATE = {"delivery", "vendor", "driver", "sweeper"}

ADVICE = {
    "Low": "Normal work. Drink water regularly.",
    "Caution": "Drink water every 30 min. Take short shade breaks.",
    "High": "Rest 10 min every hour in shade. Drink 1 cup water every 20 min.",
    "Danger": "Rest 15-20 min every hour. Avoid 12-3 PM work. Watch for dizziness.",
    "Extreme": "Stop heavy work. Move to shade/cool place. Seek medical help if unwell.",
}


def heat_index_c(temp_c: float, rh: float) -> float:
    """Heat index in Celsius (NWS Rothfusz formula)."""
    t = temp_c * 9 / 5 + 32
    simple = 0.5 * (t + 61.0 + (t - 68.0) * 1.2 + rh * 0.094)
    if (simple + t) / 2 < 80:
        hi = simple
    else:
        hi = (-42.379 + 2.04901523 * t + 10.14333127 * rh
              - 0.22475541 * t * rh - 0.00683783 * t * t
              - 0.05481717 * rh * rh + 0.00122874 * t * t * rh
              + 0.00085282 * t * rh * rh - 0.00000199 * t * t * rh * rh)
    return (hi - 32) * 5 / 9


def adjusted_index(hi_c: float, job: str) -> float:
    """Heavier physical work raises effective heat risk."""
    job = job.lower()
    if job in HEAVY:
        return hi_c + 3
    if job in MODERATE:
        return hi_c + 1.5
    return hi_c


def classify(index_c: float) -> str:
    if index_c < 27:
        return "Low"
    if index_c < 32:
        return "Caution"
    if index_c < 39:
        return "High"
    if index_c < 51:
        return "Danger"
    return "Extreme"


@app.get("/risk")
def risk(lat: float, lon: float, job: str = "construction"):
    try:
        r = requests.get(OPEN_METEO, params={
            "latitude": lat, "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m"}, timeout=10)
        r.raise_for_status()
        cur = r.json()["current"]
    except Exception:
        raise HTTPException(status_code=502, detail="Weather service unavailable")
    hi = heat_index_c(cur["temperature_2m"], cur["relative_humidity_2m"])
    adj = adjusted_index(hi, job)
    level = classify(adj)
    return {
        "temperature_c": cur["temperature_2m"],
        "humidity_pct": cur["relative_humidity_2m"],
        "heat_index_c": round(hi, 1),
        "adjusted_index_c": round(adj, 1),
        "job": job,
        "risk_level": level,
        "advice": ADVICE[level],
    }
