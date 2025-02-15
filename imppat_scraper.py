!pip install aiohttp async_timeout polars 

import asyncio
import httpx
import async_timeout
import random
import re
from urllib.parse import urljoin, quote
from bs4 import BeautifulSoup
import polars as pl
import nest_asyncio

# Patch the event loop for Colab/Jupyter environments.
nest_asyncio.apply()

# -------------------------------
# Configuration Parameters
# -------------------------------
BASE_URL = "https://cb.imsc.res.in/imppat/"
BATCH_SIZE = 10            # Process 10 plants per batch (for all plants)
REQUEST_TIMEOUT = 15       # Seconds per request
RETRY_COUNT = 3
INITIAL_DELAY = 1          # Base delay for retries in seconds
MAX_CONCURRENT_PH = 5      # Maximum concurrent phytochemical detail requests per plant

# -------------------------------
# Async Retry Helper with Exponential Backoff
# -------------------------------
async def async_retry(func, *args, retries=RETRY_COUNT, delay=INITIAL_DELAY, **kwargs):
    last_exception = None
    for attempt in range(retries):
        try:
            return await func(*args, **kwargs)
        except httpx.HTTPStatusError as e:
            if e.response is not None and e.response.status_code == 404:
                print(f"HTTP 404 in {func.__name__}: skipping URL.")
                return None
            last_exception = e
            sleep_time = delay * (2 ** attempt) * random.uniform(0.9, 1.1)
            print(f"[Retry] {func.__name__} failed: {e}. Attempt {attempt+1}/{retries} – waiting {sleep_time:.2f} sec")
            await asyncio.sleep(sleep_time)
        except Exception as e:
            last_exception = e
            sleep_time = delay * (2 ** attempt) * random.uniform(0.9, 1.1)
            print(f"[Retry] {func.__name__} failed: {e}. Attempt {attempt+1}/{retries} – waiting {sleep_time:.2f} sec")
            await asyncio.sleep(sleep_time)
    raise last_exception

# -------------------------------
# Async HTTP Helper: Get BeautifulSoup Object using HTTPX
# -------------------------------
async def async_get_soup(client: httpx.AsyncClient, url: str):
    try:
        async with async_timeout.timeout(REQUEST_TIMEOUT):
            response = await client.get(url)
            if response.status_code == 404:
                print(f"HTTP 404 for URL: {url}")
                return None
            response.raise_for_status()
            html = response.text
            try:
                return BeautifulSoup(html, "lxml")
            except Exception as e:
                print(f"Error using 'lxml': {e}. Falling back to 'html.parser'.")
                return BeautifulSoup(html, "html.parser")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        raise

# -------------------------------
# Async Function: Get All Plant Links (Alphabetically Sorted)
# -------------------------------
async def get_all_plant_links(client: httpx.AsyncClient):
    url = BASE_URL
    soup = await async_retry(async_get_soup, client, url)
    if not soup:
        raise Exception("Unable to retrieve homepage.")
    select = None
    for s in soup.find_all("select"):
        options = s.find_all("option")
        if options and len(options) > 10:
            select = s
            break
    if not select:
        raise Exception("Could not find plant drop-down on homepage.")
    plant_links = []
    for opt in select.find_all("option"):
        plant_name = opt.text.strip()
        lower_name = plant_name.lower()
        if "choose" in lower_name or "dropdown" in lower_name or lower_name.startswith("imppat |"):
            continue
        value = opt.get("value")
        if value and value.strip():
            plant_url = urljoin(BASE_URL, value)
        else:
            encoded_name = quote(plant_name)
            plant_url = urljoin(BASE_URL, f"imppat/phytochemical/{encoded_name}")
        plant_links.append((plant_name, plant_url))
    plant_links.sort(key=lambda tup: tup[0].lower())
    return plant_links

# -------------------------------
# Async Function: Parse Plant Page
# -------------------------------
async def parse_plant_page(client: httpx.AsyncClient, plant_url: str):
    soup = await async_retry(async_get_soup, client, plant_url)
    if not soup:
        return "Unknown Plant", []
    if soup.find("h1"):
        plant_name = soup.find("h1").get_text(strip=True)
    elif soup.title and soup.title.string:
        plant_name = soup.title.string.strip()
    else:
        plant_name = "Unknown Plant"
    phyto_links = []
    for a in soup.find_all("a", href=True):
        if a.text and "IMPHY" in a.text:
            detail_url = urljoin(plant_url, a["href"])
            phyto_links.append((a.text.strip(), detail_url))
    return plant_name, phyto_links

# -------------------------------
# Async Function: Parse Phytochemical Details
# -------------------------------
async def parse_phytochemical_details(client: httpx.AsyncClient, detail_url: str):
    soup = await async_retry(async_get_soup, client, detail_url)
    data = {"SMILES": "", "InChI": "", "InChIKey": "", "DeepSMILES": ""}
    if not soup:
        return data
    page_text = soup.get_text(separator="\n")
    for key in data:
        pattern = re.compile(re.escape(key) + r"\s*:\s*(.+)")
        match = pattern.search(page_text)
        if match:
            data[key] = match.group(1).strip()
    return data

# -------------------------------
# Async Function: Process One Plant (with limited concurrency for phytochemicals)
# -------------------------------
async def process_plant(client: httpx.AsyncClient, plant_tuple):
    orig_plant_name, plant_url = plant_tuple
    result = await async_retry(parse_plant_page, client, plant_url)
    if not result:
        return []
    chosen_plant, phyto_links = result
    if chosen_plant.lower().startswith("imppat |"):
        chosen_plant = orig_plant_name
    print(f"Processing Plant: {chosen_plant} — found {len(phyto_links)} phytochemical(s).")
    records = []
    ph_sem = asyncio.Semaphore(MAX_CONCURRENT_PH)

    async def process_single_ph(ph_tuple):
        ph_name, ph_url = ph_tuple
        async with ph_sem:
            details = await async_retry(parse_phytochemical_details, client, ph_url)
            return {
                "Selected plant from drop-down:": chosen_plant,
                "Processed Phytochemical Name": ph_name,
                **details,
            }

    tasks = [process_single_ph(ph) for ph in phyto_links]
    plant_records = await asyncio.gather(*tasks, return_exceptions=True)
    for rec in plant_records:
        if isinstance(rec, dict):
            records.append(rec)
    # Print a neat summary per plant.
    total = len(records)
    print(f"Processed Plant: {chosen_plant} — {total} phytochemical(s) successfully processed.")
    return records

# -------------------------------
# Async Main Function: Process All Plants in Batches
# -------------------------------
async def main_async():
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT, headers={"User-Agent": "Mozilla/5.0"}) as client:
        plant_links = await async_retry(get_all_plant_links, client)
        if not plant_links:
            raise Exception("No plant links found.")
        plant_links.sort(key=lambda tup: tup[0].lower())
        total_plants = len(plant_links)
        print(f"Found {total_plants} plants (alphabetically sorted).")

        # Divide plant links into batches of BATCH_SIZE.
        batches = [plant_links[i:i+BATCH_SIZE] for i in range(0, total_plants, BATCH_SIZE)]
        all_records = []
        batch_number = 0

        for batch in batches:
            batch_number += 1
            print(f"\nProcessing Batch {batch_number} with {len(batch)} plants...")
            tasks = [process_plant(client, plant) for plant in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for res in results:
                if isinstance(res, list) and res:
                    all_records.extend(res)
            print(f"Completed Batch {batch_number}.")
            # Delay between batches.
            await asyncio.sleep(random.uniform(3, 5))

        return all_records

# -------------------------------
# Synchronous Main Function: Run Async Loop and Write CSV
# -------------------------------
def main():
    loop = asyncio.get_event_loop()
    records = loop.run_until_complete(main_async())
    output_columns = [
        "Selected plant from drop-down:",
        "Processed Phytochemical Name",
        "SMILES",
        "InChI",
        "InChIKey",
        "DeepSMILES"
    ]
    if records:
        df = pl.DataFrame(records)
        output_csv = "imppat_all_plants.csv"
        df.write_csv(output_csv)
        print(f"\nAll records saved to {output_csv} with {len(records)} rows.")
    else:
        print("No phytochemical records were processed.")

if __name__ == "__main__":
    main()
