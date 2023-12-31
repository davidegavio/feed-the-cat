
import os
import pandas as pd
import re
import feedparser


rss_feeds_csv_path = os.path.join(
    os.path.dirname(__file__), "rss_feed.csv"
)


def get_rss_feeds():
    if not os.path.exists(rss_feeds_csv_path):
        return []
    else:
        df = pd.read_csv(rss_feeds_csv_path)
        return df.to_dict(orient="records")

    
def save_rss_feeds(rss_feeds):
    if len(rss_feeds) == 0:
        os.remove(rss_feeds_csv_path)
    else:
        pd.DataFrame(rss_feeds).to_csv(rss_feeds_csv_path, index=False)

def extract_site_name(url):
    """
    Extracts the site name from a URL, excluding the top-level domain (TLD).

    Args:
        url: The URL to extract the site name from.

    Returns:
        The site name of the URL, without the TLD.
    """

    # Compile the regular expression
    regex = re.compile(r'^(?:https?:\/\/)?(?:www\.)?([^\/\n]+)\.[^\/\n]*$')

    # Extract the site name
    match = regex.match(url)
    if match:
        return match.group(1)
    else:
        return url
    
def fetch_rss_data(url):
    feed = feedparser.parse(url)
    return list(feed.entries)