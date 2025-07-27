const fs = require('fs');
const axios = require('axios');
const { SocksProxyAgent } = require('socks-proxy-agent');
const { HttpsProxyAgent } = require('https-proxy-agent');

// ====== ALL PROXY SOURCES ======
const SOURCES = [
  // APIs
  "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http,socks4,socks5&timeout=10000&country=all&anonymity=all",
  "https://api.getproxylist.com/proxy?anonymity[]=transparent&anonymity[]=anonymous&anonymity[]=elite",
  "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc",

  // GitHub Raw & CDN Lists
  "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
  "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
  "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
  "https://raw.githubusercontent.com/gfpcom/free-proxy-list/main/list/http.txt",
  "https://raw.githubusercontent.com/gfpcom/free-proxy-list/main/list/https.txt",
  "https://raw.githubusercontent.com/gfpcom/free-proxy-list/main/list/socks4.txt",
  "https://raw.githubusercontent.com/gfpcom/free-proxy-list/main/list/socks5.txt",
  "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
  "https://raw.githubusercontent.com/hookzof/socks5_list/refs/heads/master/proxy.txt",
  "https://raw.githubusercontent.com/gitrecon1455/fresh-proxy-list/main/proxylist.txt",
  "https://raw.githubusercontent.com/databay-labs/free-proxy-list/refs/heads/master/http.txt",
  "https://raw.githubusercontent.com/databay-labs/free-proxy-list/refs/heads/master/https",
  "https://raw.githubusercontent.com/databay-labs/free-proxy-list/refs/heads/master/socks5.txt",
  "https://raw.githubusercontent.com/zenjahid/FreeProxy4u/master/http.txt",
  "https://raw.githubusercontent.com/zenjahid/FreeProxy4u/master/socks4.txt",
  "https://raw.githubusercontent.com/zenjahid/FreeProxy4u/master/socks5.txt",
  "https://raw.githubusercontent.com/shiftytr/proxy-list/master/http.txt",
  "https://raw.githubusercontent.com/shiftytr/proxy-list/master/https.txt",
  "https://raw.githubusercontent.com/shiftytr/proxy-list/master/socks4.txt",
  "https://raw.githubusercontent.com/shiftytr/proxy-list/master/socks5.txt",
  "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
  "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
  "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
  "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/http.txt",
  "https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/all.txt",
  "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt",
  "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks4.txt",
  "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks5.txt",
  "https://raw.githubusercontent.com/proxylist-to/update-list/main/http.txt",
  "https://raw.githubusercontent.com/proxylist-to/update-list/main/https.txt",
  "https://raw.githubusercontent.com/proxylist-to/update-list/main/socks4.txt",
  "https://raw.githubusercontent.com/proxylist-to/update-list/main/socks5.txt",
  "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
  "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
  "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
  "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
  "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http_proxies.txt",
  "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks4_proxies.txt",
  "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5_proxies.txt",
  "https://raw.githubusercontent.com/official-proxy/proxies/main/proxies/http.txt",
  "https://raw.githubusercontent.com/official-proxy/proxies/main/proxies/socks4.txt",
  "https://raw.githubusercontent.com/official-proxy/proxies/main/proxies/socks5.txt",
  "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt",
  "https://raw.githubusercontent.com/Zaeem20/FREE-PROXY-LIST/master/proxy_list.txt",
  "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
  "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-working-checked.txt",
  "https://raw.githubusercontent.com/sunny9577/proxy-scraper/main/proxies.txt",
  "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/proxies.txt",
  "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/proxies.txt",
  "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies_anonymous/proxies.txt",
  "https://raw.githubusercontent.com/Anonymaron/free-proxy/main/http.txt",
  "https://raw.githubusercontent.com/Anonymaron/free-proxy/main/socks4.txt",
  "https://raw.githubusercontent.com/Anonymaron/free-proxy/main/socks5.txt",
  "https://raw.githubusercontent.com/HyperBeast/proxy-list/main/http.txt",
  "https://raw.githubusercontent.com/HyperBeast/proxy-list/main/socks5.txt",
  "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
  "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt",
  "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
  "https://raw.githubusercontent.com/TuanMinhPay/Proxy-List/main/http.txt",
  "https://raw.githubusercontent.com/TuanMinhPay/Proxy-List/main/socks4.txt",
  "https://raw.githubusercontent.com/TuanMinhPay/Proxy-List/main/socks5.txt",
  "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
  "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
  "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
  "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
  "https://raw.githubusercontent.com/vmheaven/VMHeaven-Free-Proxy-Updated/refs/heads/main/http.txt",
  "https://raw.githubusercontent.com/vmheaven/VMHeaven-Free-Proxy-Updated/refs/heads/main/https.txt",
  "https://raw.githubusercontent.com/vmheaven/VMHeaven-Free-Proxy-Updated/refs/heads/main/socks4.txt",
  "https://raw.githubusercontent.com/vmheaven/VMHeaven-Free-Proxy-Updated/refs/heads/main/socks5.txt",
  "https://raw.githubusercontent.com/yemixzy/proxy-list/refs/heads/main/proxies/http.txt",
  "https://raw.githubusercontent.com/yemixzy/proxy-list/refs/heads/main/proxies/socks4.txt",
  "https://raw.githubusercontent.com/yemixzy/proxy-list/refs/heads/main/proxies/socks5.txt",
  "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/proxylist.txt",
  "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/http.txt",
  "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/https.txt",
  "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/socks4.txt",
  "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/socks5.txt",
  "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxies-Ercin/http.txt",
  "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxies-Ercin/https.txt",
  "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxies-Ercin/socks4.txt",
  "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxies-Ercin/socks5.txt",
  "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxy-KangProxy/https.txt",
  "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxy-Tsprnay/https.txt",
  "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxy-Zaeem20/https.txt",
  "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxy-hendrikbgr/proxy_list.txt",
  "https://raw.githubusercontent.com/iplocate/free-proxy-list/refs/heads/main/all-proxies.txt",
  "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/http.txt",
  "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/socks4.txt",
  "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/socks5.txt",
  "https://raw.githubusercontent.com/berkay-digital/Proxy-Scraper/refs/heads/main/proxies.txt",
  "https://raw.githubusercontent.com/variableninja/proxyscraper/refs/heads/main/proxies/http.txt",
  "https://raw.githubusercontent.com/variableninja/proxyscraper/refs/heads/main/proxies/socks.txt",
  "https://raw.githubusercontent.com/BreakingTechFr/Proxy_Free/refs/heads/main/proxies/all.txt",
  "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/refs/heads/main/proxy_files/http_proxies.txt",
  "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/refs/heads/main/proxy_files/https_proxies.txt",
  "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/refs/heads/main/proxy_files/socks4_proxies.txt",
  "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/refs/heads/main/proxy_files/socks5_proxies.txt",
  "https://raw.githubusercontent.com/Vann-Dev/proxy-list/refs/heads/main/proxies/http.txt",
  "https://raw.githubusercontent.com/Vann-Dev/proxy-list/refs/heads/main/proxies/https.txt",
  "https://raw.githubusercontent.com/Vann-Dev/proxy-list/refs/heads/main/proxies/socks4.txt",
  "https://raw.githubusercontent.com/Vann-Dev/proxy-list/refs/heads/main/proxies/socks5.txt",
  "https://raw.githubusercontent.com/sunny9577/proxy-scraper/refs/heads/master/proxies.txt",
  "https://sunny9577.github.io/proxy-scraper/generated/http_proxies.txt",
  "https://sunny9577.github.io/proxy-scraper/generated/socks4_proxies.txt",
  "https://sunny9577.github.io/proxy-scraper/generated/socks5_proxies.txt",
  "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.txt",
  "https://raw.githubusercontent.com/zloi-user/hideip.me/master/connect.txt",
  "https://raw.githubusercontent.com/zloi-user/hideip.me/master/http.txt",
  "https://raw.githubusercontent.com/zloi-user/hideip.me/master/https.txt",
  "https://raw.githubusercontent.com/zloi-user/hideip.me/master/socks4.txt",
  "https://raw.githubusercontent.com/zloi-user/hideip.me/master/socks5.txt",
  "http://multiproxy.org/txt_all/proxy.txt",
  "http://promicom.by/tools/proxy/proxy.txt",
  "http://www.socks24.org/feeds/posts/default",
  "http://globalproxies.blogspot.de/feeds/posts/default",
  "http://www.caretofun.net/free-proxies-and-socks/"
];

// ====== PROXY STORAGE ======
const proxyTypes = {
  http: new Set(),
  https: new Set(),
  socks4: new Set(),
  socks5: new Set()
};

// ====== MAIN FUNCTION ======
(async () => {
  console.log(`🚀 Starting proxy scraping from ${SOURCES.length} sources...`);
  
  // Scrape all sources
  await scrapeAllSources();
  
  // Process results
  removeDuplicates();
  saveProxies();
  
  console.log("\n✅ Scraping complete! Results:");
  console.log(`• HTTP: ${proxyTypes.http.size} proxies`);
  console.log(`• HTTPS: ${proxyTypes.https.size} proxies`);
  console.log(`• SOCKS4: ${proxyTypes.socks4.size} proxies`);
  console.log(`• SOCKS5: ${proxyTypes.socks5.size} proxies`);
})();

// ====== SCRAPING FUNCTION ======
async function scrapeAllSources() {
  const batchSize = 5; // Process 5 sources at a time
  for (let i = 0; i < SOURCES.length; i += batchSize) {
    const batch = SOURCES.slice(i, i + batchSize);
    await Promise.all(batch.map(scrapeSource));
  }
}

async function scrapeSource(url) {
  try {
    const response = await axios.get(url, { timeout: 15000 });
    const proxies = extractProxies(response.data, url);
    
    proxies.forEach(proxy => {
      const [ip, port, type] = proxy.split(':');
      if (type === 'http') proxyTypes.http.add(`${ip}:${port}`);
      else if (type === 'https') proxyTypes.https.add(`${ip}:${port}`);
      else if (type === 'socks4') proxyTypes.socks4.add(`${ip}:${port}`);
      else if (type === 'socks5') proxyTypes.socks5.add(`${ip}:${port}`);
      else proxyTypes.http.add(`${ip}:${port}`); // Default to HTTP
    });
    
    console.log(`[✔] ${url} → ${proxies.length} proxies`);
  } catch (error) {
    console.log(`[✖] ${url} → Error: ${error.message}`);
  }
}

// ====== PROXY EXTRACTION ======
function extractProxies(data, url) {
  // Enhanced pattern to detect protocol from URL if not in proxy string
  const proxyPattern = /(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{2,5})(?::(http|https|socks4|socks5))?/gi;
  const matches = [...data.matchAll(proxyPattern)];
  
  // Detect protocol from URL if needed
  let urlProtocol = '';
  if (url.includes('http.txt') || url.includes('http_proxies')) urlProtocol = 'http';
  else if (url.includes('https.txt') || url.includes('https_proxies')) urlProtocol = 'https';
  else if (url.includes('socks4.txt') || url.includes('socks4_proxies')) urlProtocol = 'socks4';
  else if (url.includes('socks5.txt') || url.includes('socks5_proxies')) urlProtocol = 'socks5';
  
  return matches.map(match => {
    const ip = match[1];
    const port = match[2];
    const type = match[3] || urlProtocol || 'http'; // Fallback to HTTP
    return `${ip}:${port}:${type}`;
  });
}

// ====== DUPLICATE REMOVAL ======
function removeDuplicates() {
  console.log("\n🧹 Removing duplicate proxies...");
  
  // Create IP:PORT map to eliminate duplicates
  const uniqueMap = new Map();
  
  // Process all proxy types
  for (const [type, proxies] of Object.entries(proxyTypes)) {
    for (const proxy of proxies) {
      const [ip, port] = proxy.split(':');
      const key = `${ip}:${port}`;
      
      if (!uniqueMap.has(key)) {
        uniqueMap.set(key, type); // Store first encountered type
      }
    }
  }
  
  // Clear existing sets
  proxyTypes.http.clear();
  proxyTypes.https.clear();
  proxyTypes.socks4.clear();
  proxyTypes.socks5.clear();
  
  // Rebuild with unique proxies
  uniqueMap.forEach((type, proxy) => {
    proxyTypes[type].add(proxy);
  });
}

// ====== SAVE RESULTS ======
function saveProxies() {
  const now = new Date();
  const dateStr = now.toISOString().split('T')[0];
  const timeStr = now.toTimeString().split(' ')[0].replace(/:/g, '-');
  
  // Create directories
  if (!fs.existsSync('proxies')) fs.mkdirSync('proxies');
  if (!fs.existsSync(`proxies/${dateStr}`)) fs.mkdirSync(`proxies/${dateStr}`);
  
  // Save each proxy type
  for (const [type, proxies] of Object.entries(proxyTypes)) {
    const cleanProxies = [...proxies].map(p => p.split(':').slice(0, 2).join(':'));
    const content = cleanProxies.join('\n');
    
    // Save latest version
    fs.writeFileSync(`proxies/${type}.txt`, content);
    
    // Save timestamped archive
    fs.writeFileSync(`proxies/${dateStr}/${type}_${timeStr}.txt`, content);
    
    console.log(`💾 Saved ${cleanProxies.length} ${type.toUpperCase()} proxies`);
  }
}
