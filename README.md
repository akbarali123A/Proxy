# GitHub Proxy Checker

This repository hosts an automated proxy checker that runs twice daily (7 AM and 7 PM) using GitHub Actions.

## Features

- Automatically fetches proxies from multiple GitHub sources
- Checks proxy functionality using Puppeteer
- Updates the working proxies list
- Hosts a simple web interface to view results

## How It Works

1. The GitHub Action runs on schedule (7 AM & 7 PM)
2. It fetches proxy lists from public GitHub repositories
3. Checks each proxy by attempting to access google.com
4. Saves working proxies to `working_proxies.txt`
5. Updates the repository with the latest results

## Viewing Results

The working proxies can be viewed:
- Directly in the repository (`working_proxies.txt`)
- Through the web interface at `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`

## Manual Run

You can manually trigger the workflow:
1. Go to "Actions" tab
2. Select "Proxy Checker" workflow
3. Click "Run workflow"
