import os
import sys
import requests

ACCESS_TOKEN = os.getenv("TOK_FB")  # Get Facebook token from environment variable
PAGE_ID = "194597373745170"  # Replace with your actual Facebook Page ID

# Kill the script if the FB_TOK is not set
if not ACCESS_TOKEN:
    print("Error: Facebook token (FB_TOK) not found. Terminating script.")
    sys.exit(1)

def get_facebook_data():
    total_reactions = 0
    total_comments = 0
    total_views = 0

    # Initial URL to get posts, including reactions and comments (WITHOUT views)
    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/posts?fields=id,likes.summary(true),comments.summary(true)&access_token={ACCESS_TOKEN}&limit=100"
    
    while url:  # Loop to handle pagination silently
        response = requests.get(url)
        data = response.json()

        if "data" in data:
            for post in data["data"]:
                post_id = post.get("id")
                likes = post.get("likes", {}).get("summary", {}).get("total_count", 0)
                comments = post.get("comments", {}).get("summary", {}).get("total_count", 0)
                views = 0  # Default if no views data found

                # Fetch post impressions separately
                insights_url = f"https://graph.facebook.com/v18.0/{post_id}/insights?metric=post_impressions&access_token={ACCESS_TOKEN}"
                insights_response = requests.get(insights_url)
                insights_data = insights_response.json()

                if "data" in insights_data:
                    for insight in insights_data["data"]:
                        if insight["name"] == "post_impressions":
                            views = insight["values"][0]["value"]

                # Add to totals
                total_reactions += likes
                total_comments += comments
                total_views += views

        # Check if there is another page of posts (pagination)
        url = data.get("paging", {}).get("next", None)

    # Output the totals to output.txt
    with open("output.txt", "w", encoding="utf-8") as file:
        output = (
            f"Total Reactions: {total_reactions}\n"
            f"Total Comments: {total_comments}\n"
            f"Total Views: {total_views}\n"
        )
        file.write(output)  # Write to output.txt

if __name__ == "__main__":
    get_facebook_data()
