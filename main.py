from integration.facebook_api import publish_post as publish_facebook_post
from integration.twitter_api import publish_tweet
from integration.tiktok_api import publish_video
from integration.linkedin_api import publish_post as publish_linkedin_post
from integration.instagram_api import publish_post as publish_instagram_post

# Funzione principale per pubblicare post su diverse piattaforme
def publish_on_platform(platform, access_token, content, extra_params=None):
    if platform == 'instagram':
        publish_instagram_post(content, access_token)
    elif platform == 'facebook':
        publish_facebook_post(extra_params['page_id'], content, access_token)
    elif platform == 'twitter':
        publish_tweet(access_token, content)
    elif platform == 'tiktok':
        publish_video(access_token, content)
    elif platform == 'linkedin':
        publish_linkedin_post(access_token, content)
    else:
        print("Piattaforma non supportata")
