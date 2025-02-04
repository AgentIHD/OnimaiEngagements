import os
import sys
import requests

ACCESS_TOKEN = os.getenv("TOK_FB")  # Get Facebook token from environment variable
PAGE_ID = "194597373745170"  # Replace with your actual Facebook Page ID

# Kill the script if the FB_TOK is not set
if not ACCESS_TOKEN:
    print("Error: Facebook token (FB_TOK) not found. Terminating script.")
    sys.exit(1)

def get_facebook_views():
    total_views = 0  # Initialize total views
    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/posts?fields=id&access_token={ACCESS_TOKEN}&limit=100"

    print("Starting Facebook Views Fetcher...")  # Debugging log

    while url:  # Loop through pages of posts
        response = requests.get(url)
        data = response.json()

        if "data" in data:
            for post in data["data"]:
                post_id = post.get("id")
                print(f"Fetching views for post: {post_id}")  # Debugging log

                # Fetch post impressions separately
                insights_url = f"https://graph.facebook.com/v18.0/{post_id}/insights?metric=post_impressions&access_token={ACCESS_TOKEN}"
                insights_response = requests.get(insights_url)
                insights_data = insights_response.json()

                print(f"Insights Response for {post_id}: {insights_data}")  # Debugging log

                # Extract views (post impressions)
                views = 0  # Default if no data found
                if "data" in insights_data:
                    for insight in insights_data["data"]:
                        if insight["name"] == "post_impressions":
                            views = insight["values"][0]["value"]

                total_views += views  # Add to total views

        # Check if there is another page of posts (pagination)
        url = data.get("paging", {}).get("next", None)

    # Output the total views to viewsoutput.txt
    with open("viewsoutput.txt", "w", encoding="utf-8") as file:
        output = f"Total Views: {total_views}\n"
        file.write(output)

    print("Total Views Fetching Completed!")  # Debugging log
    print(f"Total Views: {total_views}")  # Final result log

if __name__ == "__main__":
    get_facebook_views()
