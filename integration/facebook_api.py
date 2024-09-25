import requests
from datetime import datetime, timedelta

from utilities.token_manager import get_stored_token, is_token_expired, refresh_token

FACEBOOK_API_URL = "https://graph.facebook.com"

def publish_post(page_id, message, access_token):
    token_data = get_stored_token("instagram")

    if is_token_expired(token_data['expires_at']):
        print("Il token è scaduto. Rinnovo in corso...")
        token_data = refresh_token(token_data['access_token'], platform="instagram")

    access_token = token_data['access_token']
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
