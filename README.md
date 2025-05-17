# EPA2942 Master Thesis Maaike Kuipers

## Introduction
This project focuses on scraping and analyzing AI-generated content labels on TikTok and YouTube Shorts. It collects video URLs based on hashtags, retrieves metadata using platform APIs, and analyzes the presence and impact of AI-content labels.

The project consists of several scripts for scraping URLs, fetching metadata, and checking AI labels directly on video pages.

## Setup and Installation  

To set up the environment for running this project, follow these steps:

1. **Ensure you have Python installed on your machine.**

2. **Install Git** (required to clone repositories):  
   [Git Installation Guide](https://github.com/git-guides/install-git)  

3. **Install Playwright** (used for automated browser scraping):  
   ```bash
   pip install playwright  
   playwright install
   Playwright Documentation: https://playwright.dev/docs/intro

4. **Clone this Project to your Device**  

5. **Install required Python packages:**  
   ```bash
   pip install -r requirements.txt

6. **Store authentication cookies for YouTube (used for label scraping):**  
   - Open a terminal and run the following command to start Playwright’s code generation tool:  
     ```bash
     playwright codegen youtube.com --save-storage=YouTube/youtube_cookies.json
     ```
   - In the opened browser window:  
     - Click on **“Reject all cookies”** when prompted.  
     - Close the browser window to automatically save the cookies.

   - *Important:* Ensure that the `youtube_cookies.json` file is stored in the `YouTube` folder.  
   - This cookie file is required for authenticated access during YouTube label verification.
  
7. **Use a VPN to Simulate Geographic Locations:**  
   - To simulate different geographic locations during data collection, use a **VPN**.  
   - The VPN service used for this project was **Surfshark**, but other providers can also be used.  
   - Activate the VPN and select the target country **before** running the scraping scripts.

## How to Run the Scripts  

### 1. Scrape Hashtag Videos  

- **YouTube Shorts:**  
  ```bash
  python YouTube/hashtag_search.py
- **TikTok Videos:**
  ```bash
  python TikTok/hashtag_search.py
  
(Ensure PLATFORM and SEARCH_HASHTAG are set correctly in the script.) Repeat this for several hashtags and VPN locations.

### 2. Final Hashtag URL Check  
```bash
python final_hashtag_check.py

### 3. AI-Generated Content Label Check (YouTube Shorts Only)
  ```bash
  python YouTube/label_check.py

This script visits YouTube Shorts and checks for AI-generated content labels using Playwright.

## Notes  

- API keys and cookies are managed through variables in the scripts.  
  Ensure a valid API key is provided in `YouTube/hashtag_search.py` before running.

- Playwright may prompt for browser installation during the first run.

- Ensure that `headless = False` when running the platform-specific `hashtag_search.py` scripts.  
  This allows you to manually interact with the browser if needed.

- TikTok scraping requires manual captcha solving.  
  A 30-second pause is included in the script to handle this.


## Project Structure
<details> <summary>
├── TikTok/
│   ├── hashtag_search.py       # Scrape TikTok videos by hashtag
│   └── tiktok_api.py           # TikTok scraping and API functions
│
├── YouTube/
│   ├── hashtag_search.py       # Scrape YouTube Shorts videos by hashtag
│   ├── label_check.py          # Check AI content labels on YouTube Shorts
│   ├── youtube_api.py          # YouTube API interaction and scraping
│   └── youtube_cookies.json    # Cookies for authenticated YouTube scraping
│
├── final_hashtag_check.py      # Final check for missing URLs and metadata collection
├── requirements.txt            # Required Python packages
└── README.md                   # Project documentation
</details>

## Script Overview  

- **hashtag_search.py**  
  - Scrapes video URLs for a specific hashtag and specific platform.  
  - Saves metadata to CSV and JSON files.

- **final_hashtag_check.py**  
  - Performs a final check for missing URLs from earlier searches.  
  - Collects and stores extra metadata.

- **label_check.py**  
  - Scrapes YouTube Shorts pages to detect the presence of AI-generated content labels.  
  - Updates the dataset with `ai_label` and `sensitive_topic` flags.

- **tiktok_api.py**  
  - Handles TikTok scraping using Playwright and TikTok's API.  
  - Retrieves detailed video metadata.

- **youtube_api.py**  
  - Handles YouTube scraping and API interactions.  
  - Retrieves Shorts video metadata.

