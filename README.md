# imppat-scraper
Asynchronous web scraper for IMPPAT phytochemical data using Python (HTTPX + BeautifulSoup)

# IMPPAT Phytochemical Data Scraper

## 📜 Data Attribution  

**The scraped data** from [IMPPAT](https://cb.imsc.res.in/imppat/) is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/).  

*You must credit IMPPAT if you reuse their data.*

## 🚀 Code Usage  

**This scraper code** is provided "as-is" for educational/non-commercial purposes.  

**GitHub README Summary: Layman & Technical Explanation**

**🌱 For the Public (Layman Terms)**

**What This Project Does:**

This code is like a robot that visits the IMPPAT website, a database of Indian medicinal plants, and collects detailed chemical information (like molecular structures called SMILES) for every plant listed.

**Why It’s Useful:**

Scientists or students studying medicinal plants can use this data to research natural compounds for drug discovery, education, or conservation.

**How It Works:**

The robot processes plants in groups (batches of 500) to avoid overwhelming the website.

For each plant, it grabs all chemical data and saves it neatly into a spreadsheet (CSV).

It politely retries if the website is busy or a page is missing.

**💻 For Developers (Technical Terms)**
**What This Code Achieves:**

An asynchronous Python scraper built with HTTPX and BeautifulSoup that systematically extracts phytochemical metadata (SMILES, InChI, etc.) from IMPPAT.

**Key Features:**

Batch Processing: Processes ~4010 plants in batches (default: 500) to balance speed and server load.

Concurrency Control: Limits parallel requests using semaphores (MAX_CONCURRENT_PH = 5) to avoid throttling.

Robust Error Handling: Retries failed requests with exponential backoff and skips invalid URLs (HTTP 404).

Data Export: Outputs structured data to a CSV file using polars for efficiency.

**Technical Workflow:**

Fetch Plant Links: Scrapes the plant drop-down menu and sorts entries alphabetically.

Parse Plant Pages: For each plant, extracts all phytochemical detail page links.

Extract Chemical Data: From each phytochemical page, retrieves SMILES, InChI, InChIKey, and DeepSMILES.

Batch Processing: Uses asyncio.gather to process plants concurrently within batches.

 
