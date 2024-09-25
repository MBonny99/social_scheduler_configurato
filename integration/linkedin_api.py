import requests

LINKEDIN_API_URL = "https://api.linkedin.com/v2"

def publish_post(access_token, post_text):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "content": {
            "contentEntities": [],
            "title": post_text
        },
        "distribution": {
            "linkedInDistributionTarget": {}
        },
        "owner": f"urn:li:person:{'id_linkedin_da_inserire'}"
    }
    url = f"{LINKEDIN_API_URL}/ugcPosts"
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Errore durante la pubblicazione del post su LinkedIn: {response.text}")
