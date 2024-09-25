# token_manager.py
import requests
from datetime import datetime, timedelta

# Configurazione base per Graph API (Instagram e Facebook)
GRAPH_API_URL = "https://graph.facebook.com"
INSTAGRAM_API_URL = "https://graph.instagram.com"


# Funzione per scambiare un token breve con uno di lunga durata
def exchange_token(short_lived_token, client_secret, platform="facebook"):
    """
    Scambia un token breve con uno di lunga durata.
    """
    url = f"{GRAPH_API_URL}/oauth/access_token" if platform == "facebook" else f"{INSTAGRAM_API_URL}/access_token"
    params = {
        "grant_type": "fb_exchange_token" if platform == "facebook" else "ig_exchange_token",
        "client_secret": client_secret,
        "access_token": short_lived_token
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "access_token": data['access_token'],
            "expires_at": datetime.now() + timedelta(days=60)
        }
    else:
        raise Exception(f"Errore durante lo scambio del token su {platform}: {response.text}")


# Funzione per rinnovare il token a lunga durata
def refresh_token(long_lived_token, platform="facebook"):
    """
    Rinnova un token di lunga durata.
    """
    url = f"{GRAPH_API_URL}/oauth/access_token" if platform == "facebook" else f"{INSTAGRAM_API_URL}/refresh_access_token"
    params = {
        "grant_type": "fb_exchange_token" if platform == "facebook" else "ig_refresh_token",
        "access_token": long_lived_token
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "access_token": data['access_token'],
            "expires_at": datetime.now() + timedelta(days=60)
        }
    else:
        raise Exception(f"Errore durante il rinnovo del token su {platform}: {response.text}")


# Funzione per verificare se un token è scaduto
def is_token_expired(expiry_time):
    """
    Verifica se un token è scaduto rispetto al suo tempo di scadenza.
    """
    return datetime.now() > expiry_time


# Funzione per memorizzare i token in un file o database
def store_token(token_data, platform):
    """
    Memorizza il token in un file o database. Questa è solo una funzione mock.
    Può essere estesa per memorizzare i dati su un DB o file.
    """
    # Esempio di salvataggio in un file locale
    with open(f"{platform}_token.json", "w") as f:
        json.dump(token_data, f)

    print(f"Token per {platform} salvato correttamente.")


# Funzione per recuperare il token salvato
def get_stored_token(platform):
    """
    Recupera un token salvato da un file o database. Questa è una funzione mock.
    """
    try:
        with open(f"{platform}_token.json", "r") as f:
            token_data = json.load(f)
        return token_data
    except FileNotFoundError:
        print(f"Nessun token salvato per {platform}.")
        return None
