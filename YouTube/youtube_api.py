import requests
import pandas as pd
import re
import asyncio
import random
from playwright.async_api import async_playwright
import pandas as pd
import urllib.parse  # Import this to encode URLs
import json

BASE_URL = "https://www.googleapis.com/youtube/v3"

class YouTubeScraper:
    def __init__(self, target_urls=50, min_scrolls=5, max_scroll_attempts = 100, search_query=None, headless = False):
        self.target_urls = target_urls
        self.min_scrolls = min_scrolls
        self.max_scroll_attempts = max_scroll_attempts
        self.processed_urls = set()
        self.search_query = search_query
        self.headless = headless
        self.scroll_attempts = 0

    def encode_search_query(self, search_query):
        """Deletes the # for youtube and make it lower case for the consistency."""
        search_query = search_query.lower()
        return urllib.parse.quote(search_query[1:])

    async def scrape_urls(self):
        """Scrapes YouTube Shorts URLs using proper scrolling."""
        async with async_playwright() as p:
            encoded_search_query = self.encode_search_query(self.search_query)
            browser = await p.firefox.launch(headless=self.headless)  # Use firefox 
            context = await browser.new_context(storage_state=None) # Incognito mode
            page = await context.new_page()

            search_url = f"https://www.youtube.com/hashtag/{encoded_search_query}/shorts"

            print(f"Opening: {search_url}")
            await page.goto(search_url)

            try:
                await page.wait_for_selector("button:has-text('Reject the use of cookies and')", timeout=10000)
                await page.get_by_role("button", name="Reject all").click()
                print("Cookie rejection button clicked!")
            except:
                print("Cookie rejection button not found within 10 seconds.")

            # Wait until the page is loaded and Shorts videos appear
            await page.wait_for_load_state("networkidle")  # Wait for network to be idle
            await page.evaluate("document.body.style.zoom='50%'")  # Zoom out to 50%
            # await page.wait_for_selector("a[href*='/shorts/']", timeout=15000)
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
                videos = await page.locator("a[href*='/shorts/']").all()
                for video in videos:
                    try:
                        video_url = await video.get_attribute("href")
                        if video_url and "/shorts/" in video_url:
                            unique_results.add(video_url)
                    except Exception as e:
                        print(f"Error processing video: {e}")
                        continue  

                # **Check if new Shorts were added**
                if len(unique_results) == previous_video_count:
                    no_new_shorts_count += 1
                    print(f"No new Shorts found ({no_new_shorts_count}/{self.min_scrolls}).")
                else:
                    no_new_shorts_count = 0  

        
                if no_new_shorts_count >= self.min_scrolls:
                    print("No new Shorts found after multiple scrolls. Stopping scrolling.")
                    break  

            # FINAL CHECK: Process last batch of Shorts after scrolling stops
            print("Performing final extraction of Shorts before exiting...")
            final_videos = await page.locator("a[href*='/shorts/']").all()
            for video in final_videos:
                try:
                    video_url = await video.get_attribute("href")
                    if video_url and "/shorts/" in video_url:
                        unique_results.add(video_url)
                except Exception as e:
                    print(f"Error processing final batch: {e}")
                    continue  

            print("Finished scrolling. Extracting Shorts links...")

            # make a correct url of the unique results
            unique_results = [f"https://www.youtube.com{path}" for path in unique_results]

            # **Save Unique Shorts URLs**
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
        scroll_distance = random.randint(int(total_height * 0.3), int(total_height * 0.5))
        target_position = current_scroll_position + scroll_distance

        print(f"Scrolling from {current_scroll_position} to {target_position} / {total_height}")

        while current_scroll_position < target_position:
            step = speed + random.randint(-speed, speed)  # Randomized scroll speed
            current_scroll_position += step
            await page.evaluate(f"() => window.scrollTo(0, {current_scroll_position});")
            await asyncio.sleep(random.uniform(0.02, 0.1))  # Short pauses for smooth effect

        # **Extra delay to allow YouTube to load new content**
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

class YouTubeAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def extract_video_id(self, url):
        """Extracts video ID from a YouTube Shorts URL."""
        return url.replace('https://www.youtube.com/shorts/', '')
    
    def extract_hashtags(self, text):
        """Extracts hashtags from a text (title/description)."""
        return re.findall(r"#\w+", text) if text else []

    def fetch_video_details(self, urls, search_hashtag_set):
        """Fetches additional video details using the YouTube API."""
        video_ids = [self.extract_video_id(url) for url in urls if self.extract_video_id(url)]

        search_hashtags_lower = [] 

        for search_hashtag in search_hashtag_set:
            # Convert the search term to lowercase for case-insensitive matching
            search_hashtags_lower.append(search_hashtag.lower())

        if not video_ids:
            print("No valid video IDs found.")
            return []

        video_details = []
        request_count = 0

        for i in range(0, len(video_ids), 50):
            video_ids_batch = video_ids[i:i + 50]
            params = {
                "part": "snippet, statistics,contentDetails",
                "id": ",".join(video_ids_batch), 
                "key": self.api_key
            }
            response = requests.get(f"{BASE_URL}/videos", params=params)
            data = response.json()
            request_count += 1

            for item in data.get("items", []):
                video_id = item["id"]
                stats = item.get("statistics", {})
                snippet = item["snippet"]
                hashtags = self.extract_hashtags(snippet["title"]) + self.extract_hashtags(snippet["description"])
                hashtags_lower = [tag.lower() for tag in hashtags]  # Convert all hashtags to lowercase

                # Filter: Only include if the search term is present
                if any(search_hashtag in hashtags_lower for search_hashtag in search_hashtags_lower):
                    if f"https://www.youtube.com/shorts/{video_id}" not in {entry["url"] for entry in video_details}:  # Check whether the URL is already in the list
                        video_details.append({
                            "url": f"https://www.youtube.com/shorts/{video_id}",
                            "views": stats.get("viewCount", 0),
                            "likes": stats.get("likeCount", 0),
                            "comments": stats.get("commentCount", 0),
                            "publishedAt": snippet["publishedAt"],
                            "hashtags": hashtags # keep as list
                        })

        # print(f"Retrieved {len(video_details)} valid Shorts in {request_count} API requests.")
        return pd.DataFrame(video_details)


class LabelCheckerYouTube:
    def __init__(self, init_df_path, cookies, invalid_path, headless=False):
        self.init_df_path = init_df_path
        self.init_df = pd.read_csv(self.init_df_path)
        self.target_df = self.init_df.copy()
        self.headless = headless
        self.cookies = cookies
        self.invalid_path = invalid_path
        with open(self.invalid_path, "r") as f:
            self.invalid_urls = json.load(f)        

    async def scrape_labels(self):
        """Scrapes YouTube Shorts AI Label."""
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=self.headless)  # Use firefox 
            context = await browser.new_context(storage_state=self.cookies) # use cookies 
            page = await context.new_page()

            amount_checked_urls = 0

            # if a row does not have a label yet, check the url
            youtube_urls = self.init_df[(self.init_df['platform'] == 'youtube') & (self.init_df['ai_label'].isna())]
            
            print('starting to check urls for AI labels')
            
            # urls_to_check = [url for url in youtube_urls['url'] if url not in self.invalid_urls]
            urls_to_check = [url for url in youtube_urls['url'] if url not in self.invalid_urls]
            print (f"Found {len(urls_to_check)} URLs to check for AI labels.")
            for url in urls_to_check:
                amount_checked_urls += 1
                
                # Go to the YouTube Shorts URL
                await page.goto(url)

                try:
                    # Wait until the content div is visible
                    await page.wait_for_selector('.ytReelMetapanelViewModelHost', state='visible', timeout=20000)

                    # Retrieve the inner HTML of the content div
                    full_html = await page.content()

                    # check if the class 'ytwPlayerDisclosureViewModelHost' exists, this is a AI-generated post where content discusses sensitive topics, such as elections, ongoing conflicts and public health crises, or public officials
                    if '<span class="ytwPlayerDisclosureViewModelText">Altered or synthetic content</span>' in full_html:
                        sensitive_topic = 1
                        label = 1
                    else:
                        sensitive_topic = 0

                    # Check if the class 'ytwHowThisWasMadeSectionViewModelHost' exists within the metadata container
                    if 'ytwHowThisWasMadeSectionViewModelHost' in full_html:
                        label = 1
                    else:
                        label = 0

                    # add the label to the dataframe
                    self.target_df.loc[self.target_df['url'] == url, 'ai_label'] = label
                    self.target_df.loc[self.target_df['url'] == url, 'sensitive_topic'] = sensitive_topic

                    if amount_checked_urls % 50 == 0:
                        print(f'Checked {amount_checked_urls} urls for AI labels')
                    
                    self.target_df.to_csv(self.init_df_path, index=False)
                except:
                    print(f"Error processing video: {url}")
                    # Add the new URL if it's not already in the list
                    if url not in self.invalid_urls:
                        self.invalid_urls.append(url)

                        # Save the updated list
                        with open(self.invalid_path, "w") as f:
                            json.dump(self.invalid_urls, f)
                    continue

            # Close the browser
            await browser.close()


