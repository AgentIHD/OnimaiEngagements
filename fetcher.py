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

    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/posts?fields=id,message,created_time,likes.summary(true),comments.summary(true),insights.metric(post_impressions)&access_token={ACCESS_TOKEN}"
    
    while url:  # Loop to handle pagination
        response = requests.get(url)
        
        # Print out the response status and content for debugging
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {data}")  # Debugging print statement

        if "data" in data:
            for post in data["data"]:
                likes = post.get("likes", {}).get("summary", {}).get("total_count", 0)
                comments = post.get("comments", {}).get("summary", {}).get("total_count", 0)
                views = 0  # Default if no views data found

                # Get the views (impressions) for the post
                if "insights" in post:
                    for insight in post["insights"]["data"]:
                        if insight["name"] == "post_impressions":
                            views = insight["values"][0]["value"]

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
        print(output)  # Print to console (for debugging)
        file.write(output)  # Write to output.txt

if __name__ == "__main__":
    get_facebook_data()
