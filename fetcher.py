import os
import requests

ACCESS_TOKEN = os.getenv("FB_TOK")  # GitHub Actions Secret
PAGE_ID = "your_page_id"  # Replace with your actual Facebook Page ID

def get_facebook_data():
    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/posts?fields=id,message,created_time,likes.summary(true),comments.summary(true)&access_token={ACCESS_TOKEN}"
    response = requests.get(url)
    data = response.json()

    with open("output.txt", "w", encoding="utf-8") as file:
        for post in data.get("data", []):
            post_id = post["id"]
            message = post.get("message", "[No Text]")
            created_time = post["created_time"]
            likes = post.get("likes", {}).get("summary", {}).get("total_count", 0)
            comments = post.get("comments", {}).get("summary", {}).get("total_count", 0)

            post_info = (
                f"Post ID: {post_id}\n"
                f"Message: {message}\n"
                f"Created Time: {created_time}\n"
                f"Likes: {likes}\n"
                f"Comments: {comments}\n"
                f"{'-' * 40}\n"
            )
            
            print(post_info)  # Also print to GitHub Actions log
            file.write(post_info)  # Save to output.txt

if __name__ == "__main__":
    get_facebook_data()
