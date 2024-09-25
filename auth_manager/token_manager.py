
import json
import os
import time


class TokenManager:
    def __init__(self, token_file='tokens.json'):
        self.token_file = token_file
        if not os.path.exists(self.token_file):
            with open(self.token_file, 'w') as f:
                json.dump({}, f)

    def save_token(self, social, token, expiry):
        with open(self.token_file, 'r') as f:
            tokens = json.load(f)
        tokens[social] = {'access_token': token, 'expiry': expiry}
        with open(self.token_file, 'w') as f:
            json.dump(tokens, f)

    def get_token(self, social):
        with open(self.token_file, 'r') as f:
            tokens = json.load(f)
        return tokens.get(social, None)

    def refresh_token_if_expired(self, social):
        token_data = self.get_token(social)
        if token_data and token_data['expiry'] < time.time():
            # Implement token refresh logic if available
            pass
