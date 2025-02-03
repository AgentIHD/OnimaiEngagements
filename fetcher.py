import requests
import os
from dotenv import load_dotenv
load_dotenv()


ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
PAGE_ID = "194597373745170"


def get_facebook_data():
    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/posts?fields=id,message,created_time,likes.summary(true),comments.summary(true)&access_token={ACCESS_TOKEN}"
    response = requests.get(url)
    data = response.json()

    for post in data.get("data", []):
        post_id = post["id"]
        message = post.get("message", "[No Text]")
        created_time = post["created_time"]
        likes = post.get("likes", {}).get("summary", {}).get("total_count", 0)
        comments = post.get("comments", {}).get("summary", {}).get("total_count", 0)

        print(f"Post ID: {post_id}")
        print(f"Message: {message}")
        print(f"Created Time: {created_time}")
        print(f"Likes: {likes}")
        print(f"Comments: {comments}")
        print("-" * 40)


if __name__ == "__main__":
    get_facebook_data()
