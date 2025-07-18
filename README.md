# Bot Telegram de Paris Sportifs

Ce bot envoie chaque jour à 11h des suggestions de paris sportifs (simples et combinés), et un bilan chaque dimanche à 17h.

## Fonctionnalités
- Envoi automatique de 2 paris simples max + 1 combiné/jour.
- Bilan hebdomadaire avec taux de réussite.
- Aucun envoi si aucun match fiable.

## Installation

1. Cloner ce repo ou télécharger le zip.
2. Ajouter vos infos dans `.env` :
```
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_GROUP_ID=@your_group_id
```
3. Installer les dépendances :
```bash
pip install -r requirements.txt
```
4. Lancer le bot :
```bash
python main.py
```

Compatible Render / Railway / UptimeRobot / Replit / Fly.io