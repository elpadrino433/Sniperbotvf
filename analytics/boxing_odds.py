import os
import requests

API_ODDS_KEY = os.getenv("ODDS_API_KEY")
BASE = "https://api.the-odds-api.com/v4/sports/boxing_boxing/odds"

def get_boxing_fights():
    params = {
        "apiKey": API_ODDS_KEY,
        "regions": "us,uk,eu",
        "markets": "h2h",
        "oddsFormat": "decimal"
    }
    resp = requests.get(BASE, params=params, timeout=10)
    return resp.json()
