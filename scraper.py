#!/usr/bin/env python3
# Scraper for sailboatlistings.com
# Fetches sailboat listings and generates an RSS feed
# Related file: .github/workflows/update-feed.yml

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import re
import sys

BASE_URL = "https://www.sailboatlistings.com/sailboats_for_sale/"
FEED_TITLE = "Sailboat Listings"
FEED_DESCRIPTION = "Latest sailboat listings from sailboatlistings.com"
FEED_LINK = "https://www.sailboatlistings.com/sailboats_for_sale/"


def fetch_listings(max_listings=50):
    """Fetch sailboat listings from the website."""
    print(f"Fetching listings from {BASE_URL}...", file=sys.stderr)

    try:
        response = requests.get(BASE_URL, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"ERROR: Failed to fetch listings: {e}", file=sys.stderr)
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    listings = []

    # Find all listing tables
    for table in soup.find_all("table", width="728"):
        listing = parse_listing(table)
        if listing:
            listings.append(listing)
            if len(listings) >= max_listings:
                break

    print(f"INFO: Found {len(listings)} listings", file=sys.stderr)
    return listings


def parse_listing(table):
    """Parse a single listing table and extract information."""
    listing = {}

    try:
        # Extract title and URL
        header = table.find("span", class_="sailheader")
        if header and header.find("a"):
            listing["title"] = header.find("a").get_text(strip=True)
            listing["link"] = header.find("a")["href"]
            if not listing["link"].startswith("http"):
                listing["link"] = f"https://www.sailboatlistings.com{listing['link']}"

        # Extract specifications
        specs = table.find_all("span", class_="sailvk")
        spec_labels = table.find_all("span", class_="sailvb")

        for label, value in zip(spec_labels, specs):
            label_text = label.get_text(strip=True).replace(":", "").strip()
            value_text = value.get_text(strip=True)

            if "Length" in label_text:
                listing["length"] = value_text
            elif "Year" in label_text:
                listing["year"] = value_text
            elif "Type" in label_text:
                listing["type"] = value_text
            elif "Hull" in label_text:
                listing["hull"] = value_text
            elif "Asking" in label_text:
                listing["price"] = value_text
            elif "Location" in label_text:
                listing["location"] = value_text
            elif "Beam" in label_text:
                listing["beam"] = value_text
            elif "Draft" in label_text:
                listing["draft"] = value_text

        # Extract date added
        details = table.find("span", class_="details")
        if details:
            date_match = re.search(r"Added\s+(\d{1,2}-\w{3}-\d{4})", details.get_text())
            if date_match:
                listing["date_added"] = date_match.group(1)

        # Extract image
        img = table.find("img", alt=True)
        if img and "src" in img.attrs:
            listing["image"] = img["src"]
            if not listing["image"].startswith("http"):
                listing["image"] = f"https://www.sailboatlistings.com{listing['image']}"

        # Only return if we have minimum required fields
        if "title" in listing and "link" in listing:
            return listing

    except Exception as e:
        print(f"WARNING: Error parsing listing: {e}", file=sys.stderr)

    return None


def create_rss_feed(listings):
    """Generate RSS 2.0 feed from listings."""
    rss = ET.Element("rss", version="2.0")
    rss.set("xmlns:atom", "http://www.w3.org/2005/Atom")
    channel = ET.SubElement(rss, "channel")

    # Channel metadata
    ET.SubElement(channel, "title").text = FEED_TITLE
    ET.SubElement(channel, "link").text = FEED_LINK
    ET.SubElement(channel, "description").text = FEED_DESCRIPTION
    ET.SubElement(channel, "language").text = "en-us"
    ET.SubElement(channel, "lastBuildDate").text = datetime.utcnow().strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )

    # Self-referencing atom:link
    atom_link = ET.SubElement(channel, "{http://www.w3.org/2005/Atom}link")
    atom_link.set("href", "https://YOUR-USERNAME.github.io/sailboatlistings/feed.xml")
    atom_link.set("rel", "self")
    atom_link.set("type", "application/rss+xml")

    # Add items
    for listing in listings:
        item = ET.SubElement(channel, "item")

        # Build title
        title_parts = [listing["title"]]
        if "year" in listing:
            title_parts.append(f"({listing['year']})")
        ET.SubElement(item, "title").text = " ".join(title_parts)

        ET.SubElement(item, "link").text = listing["link"]
        ET.SubElement(item, "guid", isPermaLink="true").text = listing["link"]

        # Build description with HTML
        description = build_description(listing)
        ET.SubElement(item, "description").text = description

        # Add publication date if available
        if "date_added" in listing:
            try:
                pub_date = datetime.strptime(listing["date_added"], "%d-%b-%Y")
                ET.SubElement(item, "pubDate").text = pub_date.strftime(
                    "%a, %d %b %Y 00:00:00 GMT"
                )
            except ValueError:
                pass

    return prettify_xml(rss)


def build_description(listing):
    """Build HTML description for RSS item."""
    parts = []

    # Add image if available
    if "image" in listing:
        parts.append(
            f'<img src="{listing["image"]}" alt="{listing["title"]}" width="200"/><br/>'
        )

    # Add specifications
    specs = []
    if "price" in listing:
        specs.append(f"<b>Price:</b> {listing['price']}")
    if "length" in listing:
        specs.append(f"<b>Length:</b> {listing['length']}")
    if "year" in listing:
        specs.append(f"<b>Year:</b> {listing['year']}")
    if "type" in listing:
        specs.append(f"<b>Type:</b> {listing['type']}")
    if "hull" in listing:
        specs.append(f"<b>Hull:</b> {listing['hull']}")
    if "location" in listing:
        specs.append(f"<b>Location:</b> {listing['location']}")
    if "beam" in listing:
        specs.append(f"<b>Beam:</b> {listing['beam']}")
    if "draft" in listing:
        specs.append(f"<b>Draft:</b> {listing['draft']}")

    parts.append("<br/>".join(specs))

    return "<br/><br/>".join(parts)


def prettify_xml(elem):
    """Return a pretty-printed XML string."""
    rough_string = ET.tostring(elem, encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")


def main():
    """Main function to scrape listings and generate RSS feed."""
    print("INFO: Starting sailboat listings scraper...", file=sys.stderr)

    listings = fetch_listings(max_listings=50)

    if not listings:
        print("WARNING: No listings found!", file=sys.stderr)
        sys.exit(1)

    rss_content = create_rss_feed(listings)

    # Write to file
    output_file = "feed.xml"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rss_content)

    print(f"INFO: RSS feed generated successfully: {output_file}", file=sys.stderr)
    print(f"INFO: Feed contains {len(listings)} listings", file=sys.stderr)


if __name__ == "__main__":
    main()
