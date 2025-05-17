# EPA2942 Master Thesis Maaike Kuipers

## Introduction  

This project was developed as part of the Master Thesis for the EPA2942 course. It focuses on the automated collection and analysis of **AI-generated content labels** on **TikTok** and **YouTube Shorts**. The main goal is to explore how frequently AI-content labels appear on these platforms and assess their potential impact on user engagement.

The project pipeline automates the following tasks:  
- Scraping video URLs based on specific hashtags.  
- Retrieving detailed metadata using official and unofficial platform APIs.

This project builds upon and integrates functionalities from the following repositories:  
- [davidteather/TikTok-Api](https://github.com/davidteather/TikTok-Api) – for interacting with TikTok's API.  
- [networkdynamics/pytok](https://github.com/networkdynamics/pytok) – for TikTok scraping methodologies.

The collected data supports further statistical analyses and modeling conducted as part of the thesis research, providing insights into the prevalence of AI-generated content and its relationship with user behavior. These analyses contribute directly to the findings presented in (repository link).

## Setup and Installation  

To set up the environment for running this project, follow these steps:

1. **Ensure you have Python installed on your machine.**

2. **Install Git** (required to clone repositories):  
   [Git Installation Guide](https://github.com/git-guides/install-git)

3. **Set Up YouTube API Access:**  
   [YouTube Data API v3 Guide](https://developers.google.com/youtube/v3/getting-started)  

4. **Clone this Project to your Device**  

5. **Create and Activate a New Virtual Environment (Conda Recommended):**  
   ```bash
   conda create --name yourname-env python=3.11
   conda activate yourname-env
   ```

6. **Install required Python packages:**  
   ```bash
   pip install -r requirements.txt
   ```
7. **Install Playwright Browsers:**
   ```bash
   playwright install
   ```
8. **Store authentication cookies for YouTube (used for label scraping):**  
   - Open a terminal and run the following command to start Playwright’s code generation tool:  
     ```bash
     playwright codegen youtube.com --save-storage=YouTube/youtube_cookies.json
     ```
   - In the opened browser window:  
     - Click on **“Reject all cookies”** when prompted.  
     - Close the browser window to automatically save the cookies.

   - *Important:* Ensure that the `youtube_cookies.json` file is stored in the `YouTube` folder.  
   - This cookie file is required for authenticated access during YouTube label verification.
  
9. **Use a VPN to Simulate Geographic Locations:**  
   - To simulate different geographic locations during data collection, use a **VPN**.  
   - The VPN service used for this project was **Surfshark**, but other providers can also be used.  
   - Activate the VPN and select the target country **before** running the scraping scripts.

## How to Run the Scripts  


### Notes Before Running  

- API keys and cookies are managed through variables in the scripts.  
  Ensure that a valid API key is provided in `YouTube/hashtag_search.py` and `final_hashtag_check.py` before running.  
  Otherwise, the script will encounter errors when fetching metadata.

- Ensure that `headless = False` when running the platform-specific `hashtag_search.py` scripts.  
  This allows you to manually interact with the browser if needed.

- Before running either of the `hashtag_search.py` scripts, make sure to:  
  - Change the `COUNTRY` variable to match your active VPN location.  
  - Set the `SEARCH_HASHTAG` variable to the desired hashtag.
    The video information will be automatically saved in the following structure:
    data/{PLATFORM}/{SEARCH_HASHTAG}/{SEARCH_HASHTAG}_{COUNTRY}.csv

- **TikTok scraping requires manual captcha solving**, often triggered by the VPN location.  
A 30-second pause is included in the script to allow you to complete this.

- **YouTube scraping requires manual cookie rejection** (depending on the VPN location).  
A 10-second pause is included in the script for this action.


### 1. Scrape Hashtag Videos  

- **YouTube Shorts:**  
  ```bash
  python YouTube/hashtag_search.py
  ```
- **TikTok Videos:**
  ```bash
  python TikTok/hashtag_search.py
  ```
  
(Ensure PLATFORM and SEARCH_HASHTAG are set correctly in the script and your VPN is on) Repeat this for several hashtags and VPN locations.

### 2. Final Hashtag URL Check  
  ```bash
  python final_hashtag_check.py
  ``` 

### 3. AI-Generated Content Label Check (YouTube Shorts Only)
  ```bash
  python YouTube/label_check.py
  ```

This script visits YouTube Shorts and checks for AI-generated content labels using Playwright.


## Project Structure  
```plaintext
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
```

## Script Overview  

- **YouTube/hashtag_search.py**  
  - Scrapes YouTube Shorts video URLs for a specific hashtag.  
  - Saves metadata to CSV and JSON files.

- **TikTok/hashtag_search.py**  
  - Scrapes TikTok video URLs for a specific hashtag.  
  - Saves metadata to CSV and JSON files.
 
- **TikTok/tiktok_api.py**  
  - Handles TikTok scraping using Playwright and TikTok's API.  
  - Retrieves detailed video metadata.

- **YouTube/youtube_api.py**  
  - Handles YouTube scraping and API interactions.  
  - Retrieves Shorts video metadata.

- **final_hashtag_check.py**  
  - Performs a final check for missing URLs from earlier searches.  
  - Collects and stores extra metadata.

- **YouTube/label_check.py**  
  - Scrapes YouTube Shorts pages to detect the presence of AI-generated content labels.  
  - Updates the dataset with `ai_label` and `sensitive_topic` flags.
