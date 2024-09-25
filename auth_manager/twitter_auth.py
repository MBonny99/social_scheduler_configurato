
import requests
import time
from auth_manager.token_manager import TokenManager

class TwitterAuth:
    def __init__(self, api_key, api_secret_key, callback_uri):
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.callback_uri = callback_uri
        self.token_manager = TokenManager()

    def get_auth_url(self):
        pass

    def exchange_code_for_token(self, code):
        pass

    def refresh_token(self, refresh_token):
        pass
