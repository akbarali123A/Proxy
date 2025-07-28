import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time
import random
import re
import json
from datetime import datetime
import pytz
timestamp = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
# Configuration
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
]
TIMEOUT = 15
MAX_RETRIES = 3
TEST_URLS = ["http://httpbin.org/ip", "http://example.com"]
WORKERS = 50

def get_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

def make_request(url, proxy=None, retry=0):
    try:
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        response = requests.get(
            url,
            headers=get_headers(),
            proxies=proxies,
            timeout=TIMEOUT,
            allow_redirects=True
        )
        if response.status_code == 200:
            return response
    except Exception as e:
        if retry < MAX_RETRIES:
            time.sleep(2)
            return make_request(url, proxy, retry + 1)
    return None

def is_valid_proxy(proxy):
    for test_url in TEST_URLS:
        try:
            response = make_request(test_url, proxy)
            if response and proxy.split(':')[0] in response.text:
                return True
        except:
            continue
    return False

# ==============================================
# Scrapers for all 25 websites
# ==============================================

def scrape_geonix():
    proxies = set()
    try:
        url = "https://free.geonix.com/en/"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table#proxy-list tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.add(f"{ip}:{port}")
    except Exception as e:
        print(f"Geonix error: {e}")
    return proxies

def scrape_proxybros():
    proxies = set()
    try:
        for page in range(1, 6):
            url = f"https://proxybros.com/free-proxy-list/page/{page}/" if page > 1 else "https://proxybros.com/free-proxy-list/"
            response = make_request(url)
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                for row in soup.select('table.proxies-table tbody tr'):
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        ip = cols[0].text.strip()
                        port = cols[1].text.strip()
                        proxies.add(f"{ip}:{port}")
    except Exception as e:
        print(f"Proxybros error: {e}")
    return proxies

def scrape_iproyal():
    proxies = set()
    try:
        url = "https://iproyal.com/free-proxy-list/"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for script in soup.find_all('script'):
                if 'proxies' in script.text:
                    data = re.search(r'proxies:\s*(\[.*?\])', script.text)
                    if data:
                        proxies_data = json.loads(data.group(1))
                        for item in proxies_data:
                            proxies.add(f"{item['ip']}:{item['port']}")
    except Exception as e:
        print(f"Iproyal error: {e}")
    return proxies

def scrape_proxydb():
    proxies = set()
    try:
        url = "https://proxydb.net/"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table.table tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip_port = cols[0].find('a').text.strip()
                    proxies.add(ip_port)
    except Exception as e:
        print(f"Proxydb error: {e}")
    return proxies

def scrape_proxiware():
    proxies = set()
    try:
        url = "https://proxiware.com/free-proxy-list"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table#proxy-list tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.add(f"{ip}:{port}")
    except Exception as e:
        print(f"Proxiware error: {e}")
    return proxies

def scrape_fineproxy():
    proxies = set()
    try:
        url = "https://fineproxy.org/free-proxy/"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table.proxy-list tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.add(f"{ip}:{port}")
    except Exception as e:
        print(f"Fineproxy error: {e}")
    return proxies

def scrape_proxyrack():
    proxies = set()
    try:
        url = "https://www.proxyrack.com/free-proxy-list/"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table.proxy-table tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.add(f"{ip}:{port}")
    except Exception as e:
        print(f"Proxyrack error: {e}")
    return proxies

def scrape_lunaproxy():
    proxies = set()
    try:
        url = "https://www.lunaproxy.com/freeproxy/index.html"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table.proxy-list tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.add(f"{ip}:{port}")
    except Exception as e:
        print(f"Lunaproxy error: {e}")
    return proxies

def scrape_proxyscrape():
    proxies = set()
    try:
        url = "https://proxyscrape.com/free-proxy-list"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table.table tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.add(f"{ip}:{port}")
    except Exception as e:
        print(f"Proxyscrape error: {e}")
    return proxies

def scrape_free_proxy_list():
    proxies = set()
    try:
        url = "https://free-proxy-list.net/en/socks-proxy.html"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table#proxylisttable tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.add(f"{ip}:{port}")
    except Exception as e:
        print(f"Free-proxy-list error: {e}")
    return proxies

def scrape_proxy_list_download_socks5():
    proxies = set()
    try:
        url = "https://www.proxy-list.download/SOCKS5"
        response = make_request(url)
        if response:
            data = response.json()
            for item in data:
                proxies.add(f"{item['IP']}:{item['PORT']}")
    except Exception as e:
        print(f"Proxy-list.download SOCKS5 error: {e}")
    return proxies

def scrape_proxy_list_download_api():
    proxies = set()
    try:
        url = "https://www.proxy-list.download/api/v1/get"
        response = make_request(url)
        if response:
            for line in response.text.splitlines():
                if ':' in line:
                    proxies.add(line.strip())
    except Exception as e:
        print(f"Proxy-list.download API error: {e}")
    return proxies

def scrape_freeproxy_world():
    proxies = set()
    try:
        url = "https://www.freeproxy.world/"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table.table tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.add(f"{ip}:{port}")
    except Exception as e:
        print(f"Freeproxy.world error: {e}")
    return proxies

def scrape_proxycompass():
    proxies = set()
    try:
        url = "https://proxycompass.com/free-proxy/"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table.proxy-list tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.add(f"{ip}:{port}")
    except Exception as e:
        print(f"Proxycompass error: {e}")
    return proxies

def scrape_advanced_name():
    proxies = set()
    try:
        url = "https://advanced.name/freeproxy"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table.table tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[1].text.strip()
                    port = cols[2].text.strip()
                    proxies.add(f"{ip}:{port}")
    except Exception as e:
        print(f"Advanced.name error: {e}")
    return proxies

def scrape_iplocation():
    proxies = set()
    try:
        url = "https://www.iplocation.net/proxy-list"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table.proxy-list tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip_port = cols[0].text.strip()
                    proxies.add(ip_port)
    except Exception as e:
        print(f"Iplocation error: {e}")
    return proxies

def scrape_hidemn():
    proxies = set()
    try:
        url = "https://hide.mn/en/proxy-list"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table.proxy-list tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.add(f"{ip}:{port}")
    except Exception as e:
        print(f"Hidemn error: {e}")
    return proxies

def scrape_proxyelite():
    proxies = set()
    try:
        url = "https://proxyelite.info/free-proxy-list"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table.proxy-list tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.add(f"{ip}:{port}")
    except Exception as e:
        print(f"Proxyelite error: {e}")
    return proxies

def scrape_proxy5():
    proxies = set()
    try:
        url = "https://proxy5.net/free-proxy"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table.proxy-list tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.add(f"{ip}:{port}")
    except Exception as e:
        print(f"Proxy5 error: {e}")
    return proxies

def scrape_freeproxyupdate():
    proxies = set()
    try:
        url = "https://freeproxyupdate.com/"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table.proxy-list tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.add(f"{ip}:{port}")
    except Exception as e:
        print(f"Freeproxyupdate error: {e}")
    return proxies

def scrape_vpnside():
    proxies = set()
    try:
        url = "https://www.vpnside.com/proxy/list/"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table.proxy-list tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.add(f"{ip}:{port}")
    except Exception as e:
        print(f"Vpnside error: {e}")
    return proxies

def scrape_ditatompel():
    proxies = set()
    try:
        url = "https://www.ditatompel.com/proxy"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table.proxy-list tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.add(f"{ip}:{port}")
    except Exception as e:
        print(f"Ditatompel error: {e}")
    return proxies

def scrape_hideip():
    proxies = set()
    try:
        url = "https://hideip.me/en/proxy/"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table.proxy-list tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.add(f"{ip}:{port}")
    except Exception as e:
        print(f"Hideip error: {e}")
    return proxies

def scrape_proxyhub():
    proxies = set()
    try:
        url = "https://proxyhub.me/en/all-https-proxy-list.html"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table.proxy-list tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.add(f"{ip}:{port}")
    except Exception as e:
        print(f"Proxyhub error: {e}")
    return proxies

def scrape_proxysharp():
    proxies = set()
    try:
        url = "https://www.proxysharp.com/proxies/"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table.proxy-list tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.add(f"{ip}:{port}")
    except Exception as e:
        print(f"Proxysharp error: {e}")
    return proxies

def scrape_proxylistplus():
    proxies = set()
    try:
        url = "https://list.proxylistplus.com/"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table.proxy-list tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.add(f"{ip}:{port}")
    except Exception as e:
        print(f"Proxylistplus error: {e}")
    return proxies

def scrape_openproxylist():
    proxies = set()
    try:
        url = "https://openproxylist.com/proxy/"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table.proxy-list tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.add(f"{ip}:{port}")
    except Exception as e:
        print(f"Openproxylist error: {e}")
    return proxies

def scrape_free_proxy_cz():
    proxies = set()
    try:
        url = "http://free-proxy.cz/en/"
        response = make_request(url)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.select('table#proxy_list tbody tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip_script = cols[0].find('script')
                    if ip_script:
                        ip = re.search(r'decode\("([^"]+)"\)', ip_script.text)
                        if ip:
                            ip = ip.group(1)
                            port = cols[1].text.strip()
                            proxies.add(f"{ip}:{port}")
    except Exception as e:
        print(f"Free-proxy.cz error: {e}")
    return proxies

# ==============================================
# Main scraping function
# ==============================================

def scrape_all_sites():
    scrapers = [
        scrape_geonix,
        scrape_proxybros,
        scrape_iproyal,
        scrape_proxydb,
        scrape_proxiware,
        scrape_fineproxy,
        scrape_proxyrack,
        scrape_lunaproxy,
        scrape_proxyscrape,
        scrape_free_proxy_list,
        scrape_proxy_list_download_socks5,
        scrape_proxy_list_download_api,
        scrape_freeproxy_world,
        scrape_proxycompass,
        scrape_advanced_name,
        scrape_iplocation,
        scrape_hidemn,
        scrape_proxyelite,
        scrape_proxy5,
        scrape_freeproxyupdate,
        scrape_vpnside,
        scrape_ditatompel,
        scrape_hideip,
        scrape_proxyhub,
        scrape_proxysharp,
        scrape_proxylistplus,
        scrape_openproxylist,
        scrape_free_proxy_cz
    ]
    
    all_proxies = set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(scraper): scraper.__name__ for scraper in scrapers}
        for future in concurrent.futures.as_completed(futures):
            try:
                proxies = future.result()
                all_proxies.update(proxies)
                print(f"{futures[future]} - {len(proxies)} proxies")
            except Exception as e:
                print(f"Error in {futures[future]}: {e}")
    
    return all_proxies

# Rest of the code remains the same (check_proxies, save_results, main functions)
