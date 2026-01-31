# Architecture Overview

## System Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions                          │
│                  (Runs every 6 hours)                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   scraper.py         │
              │   - Fetch HTML       │
              │   - Parse listings   │
              │   - Generate RSS     │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   feed.xml           │
              │   (RSS 2.0 feed)     │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   Git Commit & Push  │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   GitHub Pages       │
              │   (Static hosting)   │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   RSS Readers        │
              │   - Feedly           │
              │   - NetNewsWire      │
              │   - Others           │
              └──────────────────────┘
```

## Data Flow

```
sailboatlistings.com
         │
         │ HTTP Request
         ▼
    BeautifulSoup
    HTML Parser
         │
         │ Extract data
         ▼
    Python Dict
    {title, price, ...}
         │
         │ Format as XML
         ▼
    RSS 2.0 Feed
    (feed.xml)
         │
         │ Commit to repo
         ▼
    GitHub Pages
         │
         │ HTTPS
         ▼
    Your RSS Reader
```

## Components

### scraper.py
- **Purpose**: Fetch and parse sailboat listings
- **Input**: HTML from sailboatlistings.com
- **Output**: feed.xml (RSS 2.0 format)
- **Libraries**: requests, BeautifulSoup, xml.etree
- **Run frequency**: Every 6 hours via GitHub Actions

### feed.xml
- **Format**: RSS 2.0 with Atom namespace
- **Contains**: Up to 50 latest listings
- **Fields per item**:
  - Title (boat name + year)
  - Link (to full listing)
  - Description (HTML with image and specs)
  - Publication date
  - GUID (unique identifier)

### GitHub Actions Workflow
- **File**: .github/workflows/update-feed.yml
- **Triggers**:
  - Schedule: Every 6 hours (cron)
  - Manual: workflow_dispatch
  - Push: On commits to main
- **Steps**:
  1. Check out code
  2. Install Python dependencies
  3. Run scraper
  4. Commit changes (if any)
  5. Push to repository

### GitHub Pages
- **Source**: Main branch, root directory
- **Serves**:
  - index.html (landing page)
  - feed.xml (RSS feed)
- **URL pattern**: https://USERNAME.github.io/sailboatlistings/

### index.html
- **Purpose**: User-friendly landing page
- **Features**:
  - Feed URL display
  - Usage instructions
  - RSS reader recommendations
  - Auto-updates feed URL with JavaScript

## Technology Stack

### Backend
- **Language**: Python 3.11+
- **Dependencies**:
  - beautifulsoup4: HTML parsing
  - requests: HTTP client
  - lxml: XML processing
  - xml.etree: RSS generation

### Automation
- **CI/CD**: GitHub Actions
- **Scheduler**: Cron-based triggers
- **Version Control**: Git

### Hosting
- **Platform**: GitHub Pages
- **Cost**: Free
- **SSL**: Automatic HTTPS

### Frontend
- **Landing page**: HTML + CSS + JavaScript
- **Feed format**: RSS 2.0 XML

## Security & Performance

### Rate Limiting
- Updates only every 6 hours (4x daily)
- Single page fetch per update
- Minimal server load

### Caching
- GitHub Pages serves cached content
- RSS readers cache feed data
- No database required

### Privacy
- No user data collected
- No analytics or tracking
- Public read-only access

### Error Handling
- Timeout protection (30s)
- Exception catching in parser
- Graceful degradation
- Logging to stderr

## Scalability

### Current Limits
- 50 listings per feed (configurable)
- ~27KB feed size
- 4 updates per day

### Potential Improvements
- Multi-page scraping
- Category filtering
- Price range filtering
- Location-based feeds
- Email notifications
- Database for historical tracking

## Maintenance

### Zero Maintenance Required
Once set up, the system runs automatically:
- GitHub Actions handles scheduling
- No server maintenance
- No database to manage
- No manual updates needed

### Optional Updates
- Adjust scraper if site structure changes
- Modify update frequency
- Change number of listings
- Customize RSS feed format

## Dependencies

### External Services
1. **sailboatlistings.com**: Source data
2. **GitHub**: Code hosting + Actions + Pages
3. **RSS Readers**: Feed consumption

### Risk Assessment
- **High risk**: Site structure changes (requires scraper update)
- **Medium risk**: GitHub service outages (temporary)
- **Low risk**: RSS reader compatibility (standard format)

## Monitoring

### Check Health
1. **Actions tab**: Workflow execution status
2. **Feed URL**: Verify XML is accessible
3. **Last update**: Check lastBuildDate in feed
4. **Item count**: Ensure listings are present

### Troubleshooting
- Check Actions logs for errors
- Verify site structure hasn't changed
- Test scraper locally
- Review GitHub Pages deployment status
