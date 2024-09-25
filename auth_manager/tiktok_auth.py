
import requests
import time
from auth_manager.token_manager import TokenManager

class TikTokAuth:
    def __init__(self, client_key, client_secret, redirect_uri):
        self.client_key = client_key
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_manager = TokenManager()

    def get_auth_url(self):
        return f"https://www.tiktok.com/auth/authorize?client_key={self.client_key}&scope=user.info.basic&response_type=code&redirect_uri={self.redirect_uri}"

    def exchange_code_for_token(self, code):
        url = f"https://open-api.tiktok.com/oauth/access_token/"
        payload = {
            'client_key': self.client_key,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri,
        }
        response = requests.post(url, data=payload)
        token_data = response.json()
        self.token_manager.save_token('tiktok', token_data['access_token'], time.time() + token_data['expires_in'])
        return token_data['access_token']

    def refresh_token(self, refresh_token):
        pass
