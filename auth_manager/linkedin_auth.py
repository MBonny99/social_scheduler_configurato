
import requests
import time
from auth_manager.token_manager import TokenManager

class LinkedInAuth:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_manager = TokenManager()

    def get_auth_url(self):
        return f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope=r_liteprofile,r_emailaddress,w_member_social"

    def exchange_code_for_token(self, code):
        url = f"https://www.linkedin.com/oauth/v2/accessToken"
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(url, data=payload)
        token_data = response.json()
        self.token_manager.save_token('linkedin', token_data['access_token'], time.time() + token_data['expires_in'])
        return token_data['access_token']

    def refresh_token(self, refresh_token):
        pass
