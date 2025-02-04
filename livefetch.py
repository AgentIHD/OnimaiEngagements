import os
import sys
import time
import requests
from playsound import playsound

ACCESS_TOKEN = os.getenv("TOK_FB")
PAGE_ID = "194597373745170"

if not ACCESS_TOKEN:
    print("Error: Facebook token (FB_TOK) not found. Terminating script.")
    sys.exit(1)

def get_facebook_engagement():
    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/posts?fields=id,message,likes.summary(true),comments.summary(true)&access_token={ACCESS_TOKEN}&limit=1000"

    previous_reactions = {}
    previous_comments = {}

    while True:
        response = requests.get(url)
        data = response.json()

        if "data" in data:
            for post in data["data"]:
                post_id = post.get("id")
                likes = post.get("likes", {}).get("summary", {}).get("total_count", 0)
                comments = post.get("comments", {}).get("summary", {}).get("total_count", 0)

                # Check if there are any new reactions (likes) or comments
                if post_id in previous_reactions:
                    if likes > previous_reactions[post_id]:
                        playsound("reaction_sound.mp3")  # Play reaction sound
                if post_id in previous_comments:
                    if comments > previous_comments[post_id]:
                        playsound("comment_sound.mp3")  # Play comment sound

                # Update the previous state with the latest counts
                previous_reactions[post_id] = likes
                previous_comments[post_id] = comments

        # Wait before the next check (e.g., 10 seconds)
        time.sleep(1)  # Adjust as needed to control how frequently the script checks for updates

if __name__ == "__main__":
    get_facebook_engagement()
