# Quick Start

Get your RSS feed running in 5 minutes.

## Fastest Method (Using Git)

```bash
# 1. Initialize and commit
git init
git add .
git commit -m "Initial commit"

# 2. Create repo on GitHub
# Go to: https://github.com/new
# Name: sailboatlistings
# Public repository
# Don't initialize with README

# 3. Push to GitHub
git remote add origin https://github.com/YOUR-USERNAME/sailboatlistings.git
git branch -M main
git push -u origin main

# 4. Enable on GitHub
# - Actions tab: Enable workflows
# - Settings > Pages: Enable (branch: main, folder: root)
# - Actions tab: Run "Update RSS Feed" workflow

# 5. Your feed is live at:
# https://YOUR-USERNAME.github.io/sailboatlistings/feed.xml
```

## Your Feed URL

After setup, your RSS feed will be at:
```
https://YOUR-USERNAME.github.io/sailboatlistings/feed.xml
```

Replace `YOUR-USERNAME` with your actual GitHub username.

## Add to RSS Reader

Popular readers:
- **Feedly**: https://feedly.com
- **NetNewsWire**: https://netnewswire.com (macOS/iOS)
- **NewsBlur**: https://newsblur.com

Copy your feed URL and paste it into your reader's "Add feed" option.

## Testing Locally (Optional)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scraper.py
```

Check the generated `feed.xml` file.

## Update Schedule

The feed automatically updates every 6 hours.

To change this, edit `.github/workflows/update-feed.yml`:
```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
```

Common schedules:
- Every hour: `'0 * * * *'`
- Every 12 hours: `'0 */12 * * *'`
- Daily: `'0 0 * * *'`

## Need Help?

See SETUP.md for detailed instructions.
