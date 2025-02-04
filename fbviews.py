import os
import sys
import requests

ACCESS_TOKEN = os.getenv("TOK_FB")
PAGE_ID = "194597373745170"

if not ACCESS_TOKEN:
    print("Error: Facebook token (FB_TOK) not found. Terminating script.")
    sys.exit(1)

def get_facebook_views():
    total_views = 0
    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/posts?fields=id&access_token={ACCESS_TOKEN}&limit=1000"

    print("Starting Facebook Views Fetcher...")

    while url:
        response = requests.get(url)
        data = response.json()

        if "data" in data:
            for post in data["data"]:
                post_id = post.get("id")
                print(f"Fetching views for post: {post_id}")

                insights_url = f"https://graph.facebook.com/v18.0/{post_id}/insights?metric=post_impressions&access_token={ACCESS_TOKEN}"
                insights_response = requests.get(insights_url)
                insights_data = insights_response.json()

                # Debugging
                print(f"Insights Response for {post_id}: {insights_data}")

                views = 0  
                if "data" in insights_data and insights_data["data"]:
                    for insight in insights_data["data"]:
                        if insight["name"] == "post_impressions":
                            views = insight["values"][0]["value"]
                else:
                    print(f"⚠️ No insights found for post {post_id}. Skipping...")

                total_views += views  

        url = data.get("paging", {}).get("next", None)

    # Save total views
    with open("viewsoutput.txt", "w", encoding="utf-8") as file:
        file.write(f"Total Views: {total_views}\n")

    print("Total Views Fetching Completed!")
    print(f"Total Views: {total_views}")

if __name__ == "__main__":
    get_facebook_views()
