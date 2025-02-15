# IMPPAT Phytochemical Data Scraper

**Asynchronous web scraper** for extracting phytochemical data (SMILES, InChI, etc.) from the [IMPPAT](https://cb.imsc.res.in/imppat/) database using Python (HTTPX + BeautifulSoup).

## 🌟 Key Features
- **Batch Processing**: Handles ~4010 plants in configurable batches (500/batch)
- **Error Resilience**: Auto-retry failed requests with exponential backoff
- **Parallel Processing**: Controlled concurrency for phytochemical detail pages
- **Data Export**: Generates structured CSV output using Polars

## ⚠️ Important Notes
### Data Attribution
The scraped phytochemical data is licensed under **[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)** by IMPPAT.  
*You must:*  
- Cite IMPPAT if using this data  
- Use only for **non-commercial** purposes  

### Code Usage
This scraper code is provided:
- "As-is" without warranties  
- For **educational/non-commercial** purposes  
- With no implied license for reuse  

## 🛠️ Quick Start
1. **Install requirements**:
2. **Run scraper**: python imppat_scraper.py

Output: `imppat_all_plants.csv`

## 📄 Files
- `imppat_scraper.py`: Main scraping script  
- `requirements.txt`: Dependency list  

## ⚖️ Ethical Considerations
- Respect IMPPAT's `robots.txt` and terms of service  
- Add delays between requests to avoid server overload  
- Data subject to original CC BY-NC 4.0 license




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

**Batch Processing:** Processes ~4010 plants in batches (default: 500) to balance speed and server load.

**Concurrency Control:** Limits parallel requests using semaphores (MAX_CONCURRENT_PH = 5) to avoid throttling.

**Robust Error Handling:** Retries failed requests with exponential backoff and skips invalid URLs (HTTP 404).

**Data Export:** Outputs structured data to a CSV file using polars for efficiency.

**Technical Workflow:**

**Fetch Plant Links:** Scrapes the plant drop-down menu and sorts entries alphabetically.

**Parse Plant Pages:** For each plant, extracts all phytochemical detail page links.

**Extract Chemical Data:** From each phytochemical page, retrieves SMILES, InChI, InChIKey, and DeepSMILES.

**Batch Processing:** Uses asyncio.gather to process plants concurrently within batches.

 

