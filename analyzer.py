import random

def analyze_today_matches():
    sample_matches = [
        "✅ NBA - Raptors vs Heat : Victoire Raptors",
        "✅ NHL - Canadiens vs Bruins : +5.5 buts",
        "✅ MLB - Yankees vs Red Sox : Yankees gagnent",
        "✅ BOXE - Canelo vs GGG : Canelo KO round 8",
        "✅ Soccer - CF Montréal vs Toronto FC : Moins de 2.5 buts"
    ]
    if random.random() < 0.2:
        return []
    return random.sample(sample_matches, k=min(len(sample_matches), random.randint(1, 3)))

def get_weekly_summary():
    win_simple = random.randint(5, 8)
    loss_simple = 10 - win_simple
    win_combo = 1
    loss_combo = 1
    return f"\U0001F4CA Bilan de la semaine :\n\n" \           f"Paris simples : {win_simple}W / {loss_simple}L\n" \           f"Paris combinés : {win_combo}W / {loss_combo}L\n" \           f"Taux de réussite : {round((win_simple + win_combo) / 12 * 100)}%"