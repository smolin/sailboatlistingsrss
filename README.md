# Sailboat Listings RSS Feed

Automated RSS feed generator for sailboat listings from [sailboatlistings.com](https://www.sailboatlistings.com/sailboats_for_sale/).

## Overview

This project scrapes the latest sailboat listings and generates an RSS feed that updates automatically every 6 hours. The feed can be accessed via GitHub Pages and used with any RSS reader.

## Features

- Scrapes up to 50 latest sailboat listings
- Extracts key details: price, length, year, type, location, etc.
- Includes listing images in the RSS feed
- Automatically updates every 6 hours via GitHub Actions
- Hosted on GitHub Pages for easy access

## Setup Instructions

### 1. Fork or Clone This Repository

```bash
git clone https://github.com/YOUR-USERNAME/sailboatlistings.git
cd sailboatlistings
```

### 2. Enable GitHub Actions

1. Go to your repository on GitHub
2. Click on the "Actions" tab
3. Click "I understand my workflows, go ahead and enable them"

### 3. Enable GitHub Pages

1. Go to Settings > Pages
2. Under "Source", select "Deploy from a branch"
3. Select branch: `main` and folder: `/ (root)`
4. Click "Save"

### 4. Run the Workflow Manually (First Time)

1. Go to the "Actions" tab
2. Click on "Update RSS Feed" workflow
3. Click "Run workflow" > "Run workflow"
4. Wait for it to complete

### 5. Access Your Feed

Your RSS feed will be available at:
```
https://YOUR-USERNAME.github.io/sailboatlistings/feed.xml
```

Replace `YOUR-USERNAME` with your GitHub username.

## Usage

### Add to RSS Reader

1. Copy your feed URL: `https://YOUR-USERNAME.github.io/sailboatlistings/feed.xml`
2. Open your RSS reader (Feedly, NetNewsWire, NewsBlur, etc.)
3. Add the feed using the URL

### Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run the scraper
python scraper.py

# Check the generated feed
cat feed.xml
```

## Configuration

### Update Frequency

The feed updates every 6 hours by default. To change this, edit `.github/workflows/update-feed.yml`:

```yaml
on:
  schedule:
    - cron: '0 */6 * * *'  # Change this line
```

Common cron schedules:
- Every hour: `'0 * * * *'`
- Every 12 hours: `'0 */12 * * *'`
- Daily at midnight: `'0 0 * * *'`

### Number of Listings

To change the maximum number of listings, edit `scraper.py`:

```python
listings = fetch_listings(max_listings=50)  # Change this number
```

## Project Structure

```
sailboatlistings/
├── scraper.py              # Main scraper script
├── requirements.txt        # Python dependencies
├── feed.xml               # Generated RSS feed (auto-updated)
├── index.html             # GitHub Pages landing page
├── .github/
│   └── workflows/
│       └── update-feed.yml # GitHub Actions workflow
└── README.md              # This file
```

## How It Works

1. **GitHub Actions** runs the workflow on a schedule (every 6 hours)
2. **scraper.py** fetches the sailboatlistings.com page and parses the HTML
3. Listings are extracted and formatted as RSS 2.0 XML
4. **feed.xml** is generated and committed back to the repository
5. **GitHub Pages** serves the feed at the public URL

## Troubleshooting

### Feed Not Updating

1. Check the Actions tab for workflow errors
2. Ensure GitHub Actions is enabled in your repository settings
3. Verify the workflow has write permissions (Settings > Actions > General > Workflow permissions)

### No Listings in Feed

1. Check if the website structure has changed
2. Run `python scraper.py` locally to see error messages
3. The scraper logs output to stderr for debugging

### GitHub Pages Not Working

1. Verify GitHub Pages is enabled in Settings > Pages
2. Ensure `index.html` and `feed.xml` are in the root directory
3. Wait a few minutes for GitHub Pages to deploy

## Legal and Ethical Considerations

- This scraper is for personal use only
- Respects the website's content and terms of service
- Uses reasonable request delays
- Does not overload the server (updates only every 6 hours)
- Please review sailboatlistings.com's terms of service before use

## License

This project is provided as-is for personal use. Be sure to comply with the terms of service of sailboatlistings.com.

## Contributing

Feel free to open issues or submit pull requests for improvements.
