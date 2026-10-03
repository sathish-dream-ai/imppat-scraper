# IMPPAT Phytochemical Data Scraper

**Asynchronous web scraper** for extracting phytochemical data (SMILES, InChI, etc.) from the [IMPPAT](https://cb.imsc.res.in/imppat/) database using Python (`httpx` + `BeautifulSoup`).

## 🌟 Key Features
- **Batch Processing**: Handles ~4010 plants in configurable batches (500/batch) to balance speed and server load.
- **Error Resilience**: Auto-retries failed requests with exponential backoff and gracefully skips invalid URLs (HTTP 404).
- **Parallel Processing**: Controlled concurrency using semaphores (`MAX_CONCURRENT_PH = 5`) to avoid IP throttling.
- **Data Export**: Generates structured, memory-efficient CSV output using Polars.

## ⚠️ Important Notes

### Data Attribution
The scraped phytochemical data is licensed under **[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)** by IMPPAT.  
*You must:*  
- Cite the IMPPAT database if using this data.  
- Use the data strictly for **non-commercial** purposes.  

### Code Usage
This scraper code is provided:
- "As-is" without warranties.  
- For **educational/non-commercial** purposes.  
- With no implied license for reuse.  

## 🛠️ Quick Start
1. **Install requirements**: `pip install -r requirements.txt`
2. **Run scraper**: `python imppat_scraper.py`

**Output:** `imppat_all_plants.csv`

## 📄 Files
- `imppat_scraper.py`: Main asynchronous scraping script.  
- `requirements.txt`: Dependency list (`httpx`, `beautifulsoup4`, `polars`, `asyncio`).  

## ⚖️ Ethical Considerations
- Respects IMPPAT's `robots.txt` and terms of service.  
- Includes programmed delays and concurrency limits between requests to prevent server overload.  
- Extracted data remains subject to the original CC BY-NC 4.0 license.

---

## Script Summary: Layman & Technical Explanation

### 🌱 For the Public (Layman Terms)
**What This Project Does:**
This code acts as an automated research assistant that visits the IMPPAT website (a database of Indian medicinal plants) and collects detailed chemical blueprints (like SMILES structures) for every plant listed.

**Why It’s Useful:**
Scientists, students, and pharmacologists can use this compiled data to research natural compounds for drug discovery, education, or conservation without spending months manually copying data.

**How It Works:**
- The robot processes plants in groups (batches of 500) to avoid overwhelming the website.
- For each plant, it grabs all the chemical data and saves it neatly into a spreadsheet (CSV).
- It politely waits and retries if the website is busy or a page is missing.

### 💻 For Developers (Technical Terms)
**What This Code Achieves:**
An asynchronous Python scraper built with `httpx` and `BeautifulSoup` that systematically extracts phytochemical metadata (SMILES, InChI, InChIKey, DeepSMILES) from IMPPAT.

**Technical Workflow:**
1. **Fetch Plant Links:** Scrapes the primary plant drop-down menu and sorts entries alphabetically.
2. **Parse Plant Pages:** Navigates to each plant's directory to extract all phytochemical detail page links.
3. **Extract Chemical Data:** Retrieves structural identifiers from each phytochemical page.
4. **Asynchronous Execution:** Utilizes `asyncio.gather` to process plants concurrently within batches, strictly limited by semaphores to maintain a polite crawl rate.
