import TikTok.tiktok_api as tiktok_API
import old_codes.youtube_api as youtube_API
import asyncio
import pandas as pd
import json
import os

INPUT_CSV = 'data/merged_datasets_platforms/merged_dataset_without_youtube_labels.csv'
TARGET_CSV_TIKTOK = 'data/tiktok/tiktok_extra_urls.csv'
TARGET_CSV_YOUTUBE = 'data/youtube/youtube_extra_urls.csv'
HASHTAG_JSON = f'data/hashtag_set.json'
URL_JSONS_TIKTOK = f'data/tiktok'
URL_JSONS_YOUTUBE = f'data/youtube'
COUNTRIES = ["NL", "US", "UK"]
API_KEY_YOUTUBE = "..."  # Fill in the API-key

with open(HASHTAG_JSON, 'r') as f:
    hashtag_set = json.load(f)

async def main():
    """Main function that searches for additional videos and fetches details."""

    # loop trough the urls in the input_csv
    hashtag_urls = pd.read_csv(INPUT_CSV)

    # save the urls to a list
    urls_without_final_check = hashtag_urls['url'].tolist()

    # create all tiktok and youtube links
    all_tiktok_links = []
    all_youtube_links = []

    # loop over all the urls in the json files and check whether they are in the urls_without_final_check
    for hashtag in hashtag_set:
        for country in COUNTRIES:
            with open(f'{URL_JSONS_TIKTOK}/{hashtag}/{hashtag}_{country}.json', 'r') as f:
                urls = json.load(f)
                all_tiktok_links.extend(urls)

            with open(f'{URL_JSONS_YOUTUBE}/{hashtag}/{hashtag}_{country}.json', 'r') as f:
                urls = json.load(f)
                all_youtube_links.extend(urls)

    # print the number of urls
    print("Number of urls without final check:", len(urls_without_final_check))
    print("Number of TikTok urls in the json files:", len(all_tiktok_links))
    print("Number of YouTube urls in the json files:", len(all_youtube_links))

    tiktok_urls_to_check = set()
    youtube_urls_to_check = set()

    for tiktok_link in all_tiktok_links:
        if tiktok_link not in urls_without_final_check:
            tiktok_urls_to_check.add(tiktok_link)

    for youtube_link in all_youtube_links:
        if youtube_link not in urls_without_final_check:
            youtube_urls_to_check.add(youtube_link)
    
    # print the number of urls to check
    print("Number of TikTok urls to check:", len(tiktok_urls_to_check))
    print("Number of YouTube urls to check:", len(youtube_urls_to_check))

    tiktok_api = tiktok_API.TikTokAPI()
    youtube_api = youtube_API.YouTubeAPI(API_KEY_YOUTUBE)

    # Gather information about the urls
    df_tiktok_extra_urls = await tiktok_api.fetch_video_details(tiktok_urls_to_check, search_hashtag_set=hashtag_set)

    df_tiktok_extra_urls['platform'] = 'tiktok'
    df_tiktok_extra_urls['country'] = 'extra'

    df_tiktok_extra_urls.to_csv(TARGET_CSV_TIKTOK, index=False)

    print("Video data saved successfully! in", TARGET_CSV_TIKTOK)

    df_youtube_extra_urls = youtube_api.fetch_video_details(youtube_urls_to_check, search_hashtag_set=hashtag_set)

    df_youtube_extra_urls['platform'] = 'youtube'
    df_youtube_extra_urls['country'] = 'extra'

    df_youtube_extra_urls.to_csv(TARGET_CSV_YOUTUBE, index=False)

    print("Video data saved successfully! in", TARGET_CSV_YOUTUBE)

# Run everything inside an async event loop
if __name__ == "__main__":
    asyncio.run(main())
