from flask import Flask, jsonify, request
from firebase_admin import credentials, firestore, initialize_app
import requests
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("path/to/your-firebase-adminsdk.json")
initialize_app(cred)
db = firestore.client()

# Firestore Collection reference
posts_ref = db.collection('PostDaPubblicare')


def publish_scheduled_posts():
    # Get current timestamp and the next 15 minutes
    now = datetime.datetime.utcnow()
    fifteen_minutes_later = now + datetime.timedelta(minutes=15)

    # Query Firestore for posts to be published
    posts = posts_ref.where('timestamp', '>', now).where('timestamp', '<=', fifteen_minutes_later).stream()

    for post in posts:
        post_data = post.to_dict()
        instagram_token = post_data['instagramToken']
        caption = post_data['caption']
        image_url = post_data['imageUrl']

        # Send the post to Instagram API
        response = requests.post(
            'https://graph.instagram.com/me/media',
            params={
                'access_token': instagram_token,
                'image_url': image_url,
                'caption': caption
            }
        )
        if response.status_code == 200:
            print(f"Post {post.id} published successfully.")
        else:
            print(f"Failed to publish post {post.id}. Error: {response.content}")


# Scheduler to run every 15 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(publish_scheduled_posts, 'interval', minutes=15)
scheduler.start()


@app.route('/')
def index():
    return jsonify({'message': 'Instagram Post Manager API'})


if __name__ == '__main__':
    app.run(debug=True)
