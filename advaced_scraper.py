import asyncio
import aiohttp
import re
import time
from datetime import datetime
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import json

# Extensive source list
SOURCES = [
  # APIs
  "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http,socks4,socks5&timeout=10000&country=all&anonymity=all",
  "https://api.getproxylist.com/proxy?anonymity[]=transparent&anonymity[]=anonymous&anonymity[]=elite",
  "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc",

  # GitHub Raw & CDN Lists
  "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
  "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
  "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
  # ... [include all your other sources here]
  "http://www.caretofun.net/free-proxies-and-socks/"
]

OUTPUT_FILES = {
    "http": "http_proxies.txt",
    "https": "https_proxies.txt",
    "socks4": "socks4_proxies.txt",
    "socks5": "socks5_proxies.txt"
}

TEST_URL = "http://www.google.com"
TIMEOUT = 5
CONCURRENT_REQUESTS = 100  # Number of concurrent checks
MAX_RETRIES = 2  # Retry failed sources

# Cache for already checked proxies
checked_proxies = set()

async def fetch_url(session, url):
    for attempt in range(MAX_RETRIES + 1):
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    return await response.text()
        except Exception as e:
            if attempt == MAX_RETRIES:
                print(f"Failed to fetch {url} after {MAX_RETRIES} attempts")
                return None
            await asyncio.sleep(1)

def extract_proxies(text, url):
    # Special handling for JSON APIs
    if "api.proxyscrape.com" in url or "geonode.com" in url or "getproxylist.com" in url:
        try:
            if "api.proxyscrape.com" in url:
                return text.splitlines()
            elif "geonode.com" in url:
                data = json.loads(text)
                return [f"{item['ip']}:{item['port']}" for item in data['data']]
            elif "getproxylist.com" in url:
                data = json.loads(text)
                return [f"{data['ip']}:{data['port']}"]
        except:
            pass
    
    # Default pattern for IP:PORT
    return list(set(re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', text)))

async def check_proxy(session, proxy, proxy_type):
    if proxy in checked_proxies:
        return False
        
    try:
        connector = aiohttp.TCPConnector(force_close=True)
        async with aiohttp.ClientSession(connector=connector) as test_session:
            test_proxies = {
                "http": f"{proxy_type}://{proxy}",
                "https": f"{proxy_type}://{proxy}"
            }
            try:
                async with test_session.get(TEST_URL, proxy=test_proxies['http'], timeout=TIMEOUT) as response:
                    if response.status == 200:
                        checked_proxies.add(proxy)
                        return True
            except:
                pass
    except:
        pass
    return False

async def process_source(session, url, proxy_type, results):
    text = await fetch_url(session, url)
    if text:
        proxies = extract_proxies(text, url)
        if proxies:
            print(f"Found {len(proxies)} proxies from {url}")
            
            # Check proxies in batches
            batch_size = 100
            for i in range(0, len(proxies), batch_size):
                batch = proxies[i:i + batch_size]
                tasks = [check_proxy(session, proxy, proxy_type) for proxy in batch]
                checked = await asyncio.gather(*tasks)
                
                for proxy, is_valid in zip(batch, checked):
                    if is_valid:
                        results[proxy_type].add(proxy)

def determine_proxy_type(url):
    if "http.txt" in url or "http-" in url or "http_proxies" in url:
        return "http"
    elif "https.txt" in url or "https-" in url or "https_proxies" in url:
        return "https"
    elif "socks4.txt" in url or "socks4-" in url or "socks4_proxies" in url:
        return "socks4"
    elif "socks5.txt" in url or "socks5-" in url or "socks5_proxies" in url:
        return "socks5"
    return None

async def main():
    start_time = time.time()
    results = defaultdict(set)
    
    print(f"[{datetime.now()}] Starting proxy scraping from {len(SOURCES)} sources...")
    
    connector = aiohttp.TCPConnector(limit=CONCURRENT_REQUESTS, force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for url in SOURCES:
            proxy_type = determine_proxy_type(url)
            if proxy_type:
                task = process_source(session, url, proxy_type, results)
                tasks.append(task)
        
        # Process sources in parallel
        await asyncio.gather(*tasks)
    
    # Save results
    for proxy_type, proxies in results.items():
        filename = OUTPUT_FILES[proxy_type]
        with open(filename, 'w') as f:
            f.write("\n".join(proxies))
        print(f"Saved {len(proxies)} working {proxy_type.upper()} proxies to {filename}")
    
    total_proxies = sum(len(v) for v in results.values())
    elapsed = time.time() - start_time
    print(f"\n[{datetime.now()}] Completed! Found {total_proxies} working proxies in {elapsed:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
