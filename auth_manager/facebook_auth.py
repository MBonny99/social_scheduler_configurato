
import requests
import time
from auth_manager.token_manager import TokenManager

class FacebookAuth:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_manager = TokenManager()

    def get_auth_url(self):
        return f"https://www.facebook.com/v12.0/dialog/oauth?client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope=public_profile,pages_manage_posts,pages_read_engagement"

    def exchange_code_for_token(self, code):
        url = f"https://graph.facebook.com/v12.0/oauth/access_token?client_id={self.client_id}&redirect_uri={self.redirect_uri}&client_secret={self.client_secret}&code={code}"
        response = requests.get(url)
        token_data = response.json()
        self.token_manager.save_token('facebook', token_data['access_token'], time.time() + token_data['expires_in'])
        return token_data['access_token']

    def refresh_token(self, refresh_token):
        pass
