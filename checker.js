// Load the working proxies from GitHub
async function loadProxies() {
    try {
        const response = await fetch('https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO_NAME/main/working_proxies.txt');
        if (!response.ok) throw new Error('Failed to load proxies');
        const text = await response.text();
        const proxies = text.split('\n').filter(line => line.trim());
        
        // Update UI
        document.getElementById('working-count').textContent = proxies.length;
        const proxyList = document.getElementById('proxy-list');
        proxyList.innerHTML = '';
        
        proxies.forEach(proxy => {
            const div = document.createElement('div');
            div.className = 'proxy-item';
            div.textContent = proxy;
            proxyList.appendChild(div);
        });
        
        // Update last checked time
        const lastChecked = await fetch('https://api.github.com/repos/YOUR_USERNAME/YOUR_REPO_NAME/commits?path=working_proxies.txt&per_page=1');
        const data = await lastChecked.json();
        if (data.length > 0) {
            const date = new Date(data[0].commit.committer.date);
            document.getElementById('last-checked').textContent = date.toLocaleString();
        }
    } catch (error) {
        console.error('Error loading proxies:', error);
        document.getElementById('proxy-list').innerHTML = '<div>Error loading proxy data</div>';
    }
}

// Load proxies when page loads
window.addEventListener('load', loadProxies);
