import asyncio
import random
from playwright.async_api import async_playwright
import urllib.parse  # Import this to encode URLs
from TikTokApi import TikTokApi
import datetime
import asyncio
import re
import pandas as pd
import os

class TikTokScraper:
    def __init__(self, target_urls=50, max_scrolls=2, max_scroll_attempts=100, search_query=None, headless = False):
        self.target_urls = target_urls
        self.max_scrolls = max_scrolls
        self.max_scroll_attempts = max_scroll_attempts
        self.processed_urls = set()
        self.search_query = search_query
        self.headless = headless
        self.scroll_attempts = 0

    def encode_search_query(self, search_query):
        """Deletes the # for TikTok and make it lower case for the consistency."""
        search_query = search_query.lower()
        return urllib.parse.quote(search_query[1:])

    async def scrape_urls(self):
        """Scrapes TikTok URLs using proper scrolling."""
        async with async_playwright() as p:
            encoded_search_query = self.encode_search_query(self.search_query)
            browser = await p.firefox.launch(headless=self.headless)  # Use Chromium if needed
            context = await browser.new_context(storage_state=None) # Incognito mode
            page = await context.new_page()

            search_url = f"https://www.tiktok.com/tag/{encoded_search_query}"

            print(f"Opening: {search_url}")
            await page.goto(search_url)

            # Waiting 30 seconds to solve the captcha
            print("Waiting 30 seconds to solve the captcha")
            await asyncio.sleep(30)

            # Wait until the page is loaded and tiktok videos appear
            await page.wait_for_load_state("networkidle")  # Wait for network to be idle
            await page.evaluate("document.body.style.zoom='50%'")  # Zoom out to 50%
            print("Page loaded, starting scrolling...")

            # **Step 1: Scroll Until Enough Videos Are Loaded**
            unique_results = set()
            self.scroll_attempts = 0
            no_new_shorts_count = 0  # Tracks how many times no new videos are found

            while len(unique_results) < self.target_urls and self.scroll_attempts < self.max_scroll_attempts:
                self.scroll_attempts += 1
                previous_video_count = len(unique_results)

                print(f"Scrolling... (Collected: {len(unique_results)}/{self.target_urls})")
                await self.scroll_page(page)  # Use optimized scrolling

                # **Extract Shorts URLs**
                videos = await page.locator("a[href*='/video/']").all()
                for video in videos:
                    try:
                        video_url = await video.get_attribute("href")
                        if video_url and "/video/" in video_url:

                            # Extract the username and video ID from the URL
                            parts = video_url.split("/")
                            username = parts[3]  # Username is the second element
                            video_id = parts[-1]  # Video ID is always the last element

                            # Construct the full TikTok video URL
                            formatted_url = f"https://www.tiktok.com/{username}/video/{video_id}"
                            
                            # Add the properly formatted URL to the set
                            unique_results.add(formatted_url)
                    except Exception as e:
                        print(f"Error processing video: {e}")
                        continue  

                # Check if new TikToks were added
                if len(unique_results) == previous_video_count:
                    no_new_shorts_count += 1
                    print(f"No new TikToks found ({no_new_shorts_count}/{self.max_scrolls}).")
                else:
                    no_new_shorts_count = 0  
        
                if no_new_shorts_count >= self.max_scrolls:
                    print("No new TikToks found after multiple scrolls. Stopping scrolling.")
                    break  
            
            # FINAL CHECK: Process last batch of TikToks after scrolling stops
            print("Performing final extraction of TikToks before exiting...")
            final_videos = await page.locator("a[href*='/video/']").all()

            for video in final_videos:
                try:
                    video_url = await video.get_attribute("href")

                    # Ensure the URL is not None and contains "/video/"
                    if video_url and "/video/" in video_url:
                        # Extract the username and video ID from the URL
                        parts = video_url.split("/")
                        username = parts[3]  # Username is the second element
                        video_id = parts[-1]  # Video ID is always the last element

                        # Construct the full TikTok video URL
                        formatted_url = f"https://www.tiktok.com/{username}/video/{video_id}"

                        # Add the properly formatted URL to the set
                        unique_results.add(formatted_url)

                except Exception as e:
                    print(f"Error processing video: {e}")
                    continue

            print("Finished scrolling. Extracting TikTok links...")
            print(f"Total unique TikTok URLs found: {len(unique_results)}")

            # **Step 2: Save Unique Shorts URLs**
            results_list = list(unique_results)

            await browser.close()

            return results_list

    async def scroll_page(self, page, speed=10):
        """Smoothly scrolls down the page with a variable speed."""
        current_scroll_position = await page.evaluate(
            "() => document.documentElement.scrollTop || document.body.scrollTop;")
        total_height = await page.evaluate(
            "() => document.documentElement.scrollHeight || document.body.scrollHeight;")

        # Scroll between 30-50% of the total page height
        scroll_distance = random.randint(int(total_height * 0.2), int(total_height * 0.8))
        target_position = current_scroll_position + scroll_distance

        print(f"Scrolling from {current_scroll_position} to {target_position} / {total_height}")

        while current_scroll_position < target_position:
            step = speed + random.randint(-speed, speed)  # Randomized scroll speed
            current_scroll_position += step
            await page.evaluate(f"() => window.scrollTo(0, {current_scroll_position});")
            await asyncio.sleep(random.uniform(0.02, 0.1))  # Short pauses for smooth effect

        # **Extra delay to allow TikTok to load new content**
        await asyncio.sleep(random.uniform(2, 4))  

        # **Pause briefly every 5 scrolls to make it not too agressive**
        if self.scroll_attempts % 5 == 0:
            print("Pausing briefly to make it not too agressive...")
            await asyncio.sleep(random.uniform(5, 8))

    async def slight_scroll_up(self, page, speed=10):
        """Smoothly scrolls up slightly to refresh content."""
        desired_scroll = -300  # Amount to scroll up
        current_scroll = 0

        print(f"Smooth scrolling up by {desired_scroll} pixels")

        while current_scroll > desired_scroll:
            step = speed + random.randint(-speed, speed)  # Randomized speed for a natural effect
            current_scroll -= step
            await page.evaluate(f"() => window.scrollBy(0, {-step});")
            await asyncio.sleep(random.uniform(0.02, 0.1))  # Short pauses for smooth effect

class TikTokAPI: 
    def __init__(self):
        self.ms_token = os.environ.get("ms_token", None)  # Set your own ms_token
        
    async def fetch_video_details(self, urls, search_hashtag_set):
        """Fetches details for each TikTok video and returns a DataFrame."""

        search_hashtags_lower = [] 

        for search_hashtag in search_hashtag_set:
            # Convert the search term to lowercase for case-insensitive matching
            search_hashtags_lower.append(search_hashtag.lower())

        async with TikTokApi() as api:
            data_list = []
            info_gathered = 0
            
            await api.create_sessions(
                ms_tokens=[self.ms_token], num_sessions=1, sleep_after=3, 
                browser=os.getenv("TIKTOK_BROWSER", "chromium"), headless=False
            )

            for url in urls:
                try:
                    video = api.video(url=url)
                    video_info = await video.info()  # Fetch video details
                    info_gathered += 1
                    
                    # Extract author and stats data
                    stats = video_info.get('statsV2', {})

                    tiktok_link = url # Keep the original URL	
                    
                    # Extract additional video details
                    ai_label = video_info.get('aigcLabelType', 0)  # AI-generated content label
                    contents = video_info.get('contents', '')  # Video content description
                    hashtags = re.findall(r"#\w+", str(contents)) if contents else []  # Extract hashtags
                    create_time = video_info.get('createTime', 'unknown')  # Get video creation time
                    
                    # Extract engagement metrics
                    likes = stats.get("diggCount", 0)
                    comments = stats.get("commentCount", 0)
                    shares = stats.get("shareCount", 0)
                    views = stats.get("playCount", 0)
                    
                    hashtags_lower = [tag.lower() for tag in hashtags]  # Convert all hashtags to lowercase

                    # Filter: Only include if the search term is present
                    if any(search_hashtag in hashtags_lower for search_hashtag in search_hashtags_lower):
                        if tiktok_link not in {entry["url"] for entry in data_list}:  # Check whether the URL is already in the list
                            # Append extracted data to the list
                            data_list.append({
                                "url": tiktok_link,
                                "ai_label": ai_label,
                                "views": views,
                                "likes": likes,
                                "comments": comments,
                                "shares": shares,
                                "hashtags": hashtags,
                                "publishedAt" : datetime.datetime.fromtimestamp(int(create_time)).strftime('%Y-%m-%d %H:%M:%S')
                            })

                    if info_gathered % 25 == 0:
                        print(f"Processed {info_gathered} videos...")

                except Exception as e:
                    print(f"Error fetching video info for {url}: {e}")

            print(f"Total videos processed: {len(data_list)}")
        
        return pd.DataFrame(data_list)