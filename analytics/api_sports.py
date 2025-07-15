import os
import requests

API_SPORTS_KEY = os.getenv("API_SPORTS_KEY")
BASE = "https://v1.api-sports.io"
HEADERS = {"x-apisports-key": API_SPORTS_KEY}

def get_upcoming(sport, league_id=None):
    url = f"{BASE}/{sport}/fixtures"
    params = {"next": 5}
    if league_id:
        params["league"] = league_id
    resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
    data = resp.json()
    return data.get("response", [])

def get_odds(sport, fixture_id):
    url = f"{BASE}/{sport}/odds"
    params = {"fixture": fixture_id}
    resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
    data = resp.json()
    return data.get("response", [])
