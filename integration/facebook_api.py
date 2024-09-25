# integrations/facebook_api.py
import requests
from datetime import datetime, timedelta

# Endpoint della Graph API per Facebook
FACEBOOK_API_URL = "https://graph.facebook.com"

# Funzione per scambiare il token breve con uno di lunga durata
def exchange_token(short_lived_token, client_secret):
    url = f"{FACEBOOK_API_URL}/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_secret": client_secret,
        "fb_exchange_token": short_lived_token
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['access_token'], datetime.now() + timedelta(days=60)
    else:
        raise Exception("Errore durante lo scambio del token")

# Funzione per rinnovare il token di lunga durata
def refresh_token(long_lived_token, client_id, client_secret):
    url = f"{FACEBOOK_API_URL}/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "fb_exchange_token": long_lived_token
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['access_token'], datetime.now() + timedelta(days=60)
    else:
        raise Exception("Errore durante il rinnovo del token")

# Funzione per pubblicare un post su una pagina Facebook
def publish_post(page_id, message, access_token):
    url = f"{FACEBOOK_API_URL}/{page_id}/feed"
    params = {
        "message": message,
        "access_token": access_token
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Errore nella pubblicazione del post su Facebook")
