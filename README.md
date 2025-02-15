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



