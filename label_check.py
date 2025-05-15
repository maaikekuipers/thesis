import youtube_api as api  # Import the functions from youtube.py
import pandas as pd
import asyncio

INIT_CSV_PATH = 'data/merged_datasets_platforms/merged_dataset_with_youtube_labels.csv'
COOKIES_JSON = 'YouTube/youtube_cookies.json'
INVALID_PATH = 'data/youtube_invalid_urls.json'

async def main():
    """
    Main function looks for the AI labels in the videos.
    """ 
    # Create an instance of the YouTube_label_check class
    youtube_api = api.LabelCheckerYouTube(init_df_path=INIT_CSV_PATH, cookies=COOKIES_JSON, invalid_path = INVALID_PATH)

    await youtube_api.scrape_labels()

    print("Video data saved successfully! in", INIT_CSV_PATH)

# Run everything inside an async event loop
if __name__ == "__main__":
    asyncio.run(main())