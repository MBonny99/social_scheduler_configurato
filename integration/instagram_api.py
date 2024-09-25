# integrations/instagram_api.py
import requests

from utilities.token_manager import exchange_token, refresh_token, get_stored_token, is_token_expired, INSTAGRAM_API_URL


def publish_post(media_id):
    # Recupera il token salvato
    token_data = get_stored_token("instagram")

    # Verifica se il token è scaduto
    if is_token_expired(token_data['expires_at']):
        print("Il token è scaduto. Rinnovo in corso...")
        token_data = refresh_token(token_data['access_token'], platform="instagram")

    # Usa il token rinnovato o originale
    access_token = token_data['access_token']

    url = f"{INSTAGRAM_API_URL}/me/media_publish"
    params = {
        "creation_id": media_id,
        "access_token": access_token
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Errore nella pubblicazione del post su Instagram")
