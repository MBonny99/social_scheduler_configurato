import requests

TWITTER_API_URL = "https://api.twitter.com/2/tweets"

def publish_tweet(access_token, tweet_text):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "text": tweet_text
    }
    response = requests.post(TWITTER_API_URL, headers=headers, json=data)
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Errore durante la pubblicazione del tweet: {response.text}")
