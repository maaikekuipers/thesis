import youtube_api as api
import asyncio
import pandas as pd
import json
import os

PLATFORM = 'youtube'
COUNTRY = "UK"
SEARCH_HASHTAG = "#aiartist"  # Change to the target hashtag
TOTAL_VIDEOS_NEEDED = 250  # Number of videos to gather

TARGET_CSV = f'data/{PLATFORM}/{SEARCH_HASHTAG}/{SEARCH_HASHTAG}_{COUNTRY}.csv'
TARGET_JSON = f'data/{PLATFORM}/{SEARCH_HASHTAG}/{SEARCH_HASHTAG}_{COUNTRY}.json'
HASHTAG_JSON = f'data/hashtag_set.json'
TARGET_FOLDER = f'data/{PLATFORM}/{SEARCH_HASHTAG}'

with open(HASHTAG_JSON, 'r') as f:
    hashtag_set = json.load(f)

if SEARCH_HASHTAG not in hashtag_set:
    hashtag_set.append(SEARCH_HASHTAG)

# save new json with new hashtag
with open(HASHTAG_JSON, 'w') as f:
    json.dump(hashtag_set, f, indent=4)  

API_KEY = "AIzaSyATkdqf9FkrH4zuzf56_JdXB3ug2NY67Oo" # Fill in the API-key

async def main():
    """
    Main function that searches for Shorts videos and saves results to CSV.
    """
    # Create the target folder if it doesn't exist
    os.makedirs(TARGET_FOLDER, exist_ok=True)

    # Create an instance of the YouTubeScraper class
    scraper = api.YouTubeScraper(target_urls=TOTAL_VIDEOS_NEEDED, search_query=SEARCH_HASHTAG, headless=False)

    # Run the scrape function and retrieve the DataFrame
    urls = await scraper.scrape_urls()

    # Export the URLs as JSON
    with open(TARGET_JSON, 'w') as f:
        json.dump(urls, f)

    # Create an instance of the YouTubeAPI class
    youtube_api = api.YouTubeAPI(API_KEY)

    # Gather information about the URLs
    df = youtube_api.fetch_video_details(urls, search_hashtag_set=hashtag_set)

    # add a column country with the value of COUNTRY
    df['country'] = COUNTRY

    # add a column with the platform
    df['platform'] = PLATFORM

    # Save to CSV
    df.to_csv(TARGET_CSV, index=False)

    print("Video data saved successfully! in", TARGET_CSV)


# Run everything inside an async event loop
if __name__ == "__main__":
    asyncio.run(main())