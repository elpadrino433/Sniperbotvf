import requests
from bs4 import BeautifulSoup

def get_form(team_name):
    try:
        url = f"https://www.soccerstats.com/team.asp?league=england&team={team_name.replace(' ', '-').lower()}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, 'html.parser')

        results = soup.select('td[width="20"] font[color]')
        recent = [res.get_text(strip=True) for res in results[:5]]
        score = sum(3 if r == 'W' else 1 if r == 'D' else 0 for r in recent)

        return score, recent
    except Exception as e:
        return 0, []

def analyze_match(team1, team2):
    score1, form1 = get_form(team1)
    score2, form2 = get_form(team2)

    if score1 > score2:
        jouer = team1
        commentaire = f"{team1} est en meilleure forme ({score1} pts vs {score2})"
    elif score2 > score1:
        jouer = team2
        commentaire = f"{team2} est en meilleure forme ({score2} pts vs {score1})"
    else:
        jouer = team1
        commentaire = "Forme similaire, on mise sur l'équipe à domicile (par défaut)"

    return {
        "jouer": jouer,
        "form1": score1,
        "form2": score2,
        "commentaire": commentaire
    }
