# Setup Guide

Follow these steps to get your sailboat listings RSS feed up and running.

## Prerequisites

- A GitHub account
- Git installed on your computer (optional, can use GitHub web interface)

## Step-by-Step Setup

### Option A: Using Git Command Line

1. **Initialize Git Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Sailboat listings RSS feed scraper"
   ```

2. **Create GitHub Repository**
   - Go to https://github.com/new
   - Repository name: `sailboatlistings`
   - Description: "RSS feed for sailboat listings"
   - Make it Public (required for GitHub Pages)
   - Do NOT initialize with README (we already have one)
   - Click "Create repository"

3. **Push to GitHub**
   ```bash
   git remote add origin https://github.com/YOUR-USERNAME/sailboatlistings.git
   git branch -M main
   git push -u origin main
   ```
   Replace `YOUR-USERNAME` with your GitHub username.

4. **Enable GitHub Actions**
   - Go to your repository on GitHub
   - Click "Actions" tab
   - Click "I understand my workflows, go ahead and enable them"

5. **Enable GitHub Pages**
   - Go to Settings > Pages
   - Source: "Deploy from a branch"
   - Branch: `main`
   - Folder: `/ (root)`
   - Click "Save"

6. **Run First Update**
   - Go to "Actions" tab
   - Click "Update RSS Feed"
   - Click "Run workflow" > "Run workflow"
   - Wait for completion (should take 30-60 seconds)

7. **Access Your Feed**
   Your feed will be available at:
   ```
   https://YOUR-USERNAME.github.io/sailboatlistings/feed.xml
   ```

### Option B: Using GitHub Web Interface

1. **Create New Repository**
   - Go to https://github.com/new
   - Repository name: `sailboatlistings`
   - Description: "RSS feed for sailboat listings"
   - Make it Public
   - Click "Create repository"

2. **Upload Files**
   - Click "uploading an existing file"
   - Drag and drop all files from this directory EXCEPT:
     - `venv/` folder (if present)
     - `.ruff_cache/` folder (if present)
   - Commit message: "Initial commit: Sailboat listings RSS feed scraper"
   - Click "Commit changes"

3. **Enable GitHub Actions**
   - Click "Actions" tab
   - Click "I understand my workflows, go ahead and enable them"

4. **Enable GitHub Pages**
   - Go to Settings > Pages
   - Source: "Deploy from a branch"
   - Branch: `main`
   - Folder: `/ (root)`
   - Click "Save"

5. **Run First Update**
   - Go to "Actions" tab
   - Click "Update RSS Feed"
   - Click "Run workflow" > "Run workflow"
   - Wait for completion

6. **Access Your Feed**
   ```
   https://YOUR-USERNAME.github.io/sailboatlistings/feed.xml
   ```

## Verification

1. **Check Actions**: Go to Actions tab and verify the workflow ran successfully
2. **Check Pages**: Go to Settings > Pages and note the URL
3. **Test Feed**: Visit `https://YOUR-USERNAME.github.io/sailboatlistings/feed.xml`
4. **Check Landing Page**: Visit `https://YOUR-USERNAME.github.io/sailboatlistings/`

## Troubleshooting

### Actions Not Running
- Ensure repository is public
- Check Settings > Actions > General > Workflow permissions
- Should be set to "Read and write permissions"

### Pages Not Deploying
- Wait 2-3 minutes after enabling Pages
- Check Settings > Pages for deployment status
- Ensure `index.html` is in root directory

### Feed Not Updating
- Check Actions tab for errors
- Click on failed workflow to see error details
- Verify `requirements.txt` and `scraper.py` were uploaded

## Next Steps

After setup:
1. Add the feed to your RSS reader
2. Customize update frequency in `.github/workflows/update-feed.yml`
3. Adjust number of listings in `scraper.py`
4. Share your feed URL with friends

## Support

If you encounter issues:
1. Check the Actions tab for workflow logs
2. Review the README.md troubleshooting section
3. Create an issue on GitHub
