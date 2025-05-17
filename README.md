# EPA2942 Master Thesis Maaike Kuipers
install git: https://github.com/git-guides/install-git
terminal run (kan ook in de requirements trouwens) pip install git+https://github.com/davidteather/TikTok-Api.git 

dit werrkkttt :) 

## Introduction
This project focuses on scraping and analyzing AI-generated content labels on TikTok and YouTube Shorts. It collects video URLs based on hashtags, retrieves metadata using platform APIs, and analyzes the presence and impact of AI-content labels.

The project consists of several scripts for scraping URLs, fetching metadata, and checking AI labels directly on video pages.

## Setup and Installation
To set up the environment for running this project, follow these steps:

1. Ensure you have Python installed on your machine.

2. Install Git (required to clone repositories):
   Git Installation Guide: https://github.com/git-guides/install-git

3. Install Playwright (used for automated browser scraping):
   Playwright Documentation: https://playwright.dev/docs/intro

4. Set up YouTube API Access (required for fetching video metadata):
   YouTube Data API v3 Guide: https://developers.google.com/youtube/v3/getting-started

5. Clone or download the project files to your local machine.

6. Open a terminal and navigate to the project directory.

7. Install required Python packages:
   pip install -r requirements.txt

## How to Run the Scripts

1. Scrape Hashtag Videos
- YouTube Shorts:
  python hashtag_search.py
- TikTok Videos:
  python hashtag_search.py
  (Ensure PLATFORM and SEARCH_HASHTAG are set correctly in the script.)

2. Final Hashtag URL Check
  python final_hashtag_check.py

3. AI-Generated Content Label Check (YouTube Shorts Only)
  python label_check.py

This script visits YouTube Shorts and checks for AI-generated content labels using Playwright.

## Notes

- API keys and cookies are managed through variables in the scripts. Ensure valid API keys are in place before running.
- Playwright may prompt for browser installation during the first run.
- TikTok scraping requires manual captcha solving. A 30-second pause is included to handle this.

## Project Structure

├── data/                         # Contains input/output datasets and JSON files
│   ├── hashtag_set.json          # Maintains the list of searched hashtags
│   └── ...                       # Folder structure for TikTok and YouTube data
├── final_hashtag_check.py        # Final check for missing URLs and metadata collection
├── hashtag_search.py             # Script to scrape videos based on hashtags (YouTube or TikTok)
├── label_check.py                # Checks for AI-generated content labels on YouTube Shorts
├── tiktok_api.py                 # TikTok scraping and API interaction module
└── youtube_api.py                # YouTube scraping and API interaction module

Script Overview

- hashtag_search.py
  - Scrapes video URLs for a specific hashtag.
  - Saves metadata to CSV and JSON files.
  - Supports both TikTok and YouTube (edit PLATFORM and SEARCH_HASHTAG).

- final_hashtag_check.py
  - Performs a final check for missing URLs from earlier searches.
  - Collects and stores extra metadata.

- label_check.py
  - Scrapes YouTube Shorts pages to detect the presence of AI-generated content labels.
  - Updates the dataset with ai_label and sensitive_topic flags.

- tiktok_api.py
  - Handles TikTok scraping using Playwright and TikTok's API.
  - Retrieves detailed video metadata.

- youtube_api.py
  - Handles YouTube scraping and API interactions.
  - Retrieves Shorts video metadata and engagement statistics.
