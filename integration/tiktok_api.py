# integrations/tiktok_api.py
import requests

TIKTOK_API_URL = "https://open-api.tiktok.com"

# Funzione per pubblicare un video su TikTok
def publish_video(access_token, video_url):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "video_url": video_url
    }
    url = f"{TIKTOK_API_URL}/video/publish"
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Errore durante la pubblicazione del video su TikTok: {response.text}")
