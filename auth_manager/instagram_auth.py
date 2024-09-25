
import requests
import time
from auth_manager.token_manager import TokenManager

class InstagramAuth:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_manager = TokenManager()

    def get_auth_url(self):
        return f"https://api.instagram.com/oauth/authorize?client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope=user_profile,user_media&response_type=code"

    def exchange_code_for_token(self, code):
        url = "https://api.instagram.com/oauth/access_token"
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri,
            'code': code
        }
        response = requests.post(url, data=payload)
        token_data = response.json()
        self.token_manager.save_token('instagram', token_data['access_token'], time.time() + token_data['expires_in'])
        return token_data['access_token']

    def refresh_token(self, refresh_token):
        pass
