import time

from cat.log import log
from cat.mad_hatter.decorators import hook, tool

from .rss_feed import (extract_site_name, fetch_rss_data, get_rss_feeds,
                       save_rss_feeds)


@tool(return_direct=True)
def add_rss_feed(feed, cat):
    """
        Add item to the rss feed list. 
        User may say: 
            - "Add the RSS feed [feed] to the list"
            - "Include [feed] in the RSS feeds"
            - "Add an RSS feed with the URL [feed]"
            - "I would like to add [feed] to the RSS feed list"
            -  or similar even in other languages
        Argument [feed] is a string representing the item
    """
    name = extract_site_name(url=feed)
    rss_feeds = get_rss_feeds()
    rss_feeds.append({
        "created": time.time(),
        "name": name,
        "url": str(feed)
    })
    save_rss_feeds(rss_feeds)

    return f"RSS feed list updated with: *{feed}* and name *{name}*"

@tool(return_direct=True)
def get_feed_list(cat):
    """
        Shows all the items in the rss feed list. 
        User may say: 
            - "Show me my RSS feed list"
            - "What's inside my RSS feed list"
            -  or similar even in other languages
    """
    rss_feeds = get_rss_feeds()
    return rss_feeds

@tool(return_direct=True)
def remove_rss_feed(name, cat):
    """
        Remove an item from the rss feed list. 
        User may say: 
            - "Remove the RSS feed [name] from the list"
            - "Remove [name] from the RSS feeds"
            - "Remove an RSS feed with the name [name]"
            - "I would like to remove [name] from the RSS feed list"
            -  or similar even in other languages
        Argument [name] is a string representing the item
    """
    rss_feeds = get_rss_feeds()
    len_original_feed_list = len(rss_feeds)
    rss_feeds = [feed for feed in rss_feeds if name not in feed["name"]]
    len_updated_feed_list = len(rss_feeds)
    save_rss_feeds(rss_feeds)

    if len_original_feed_list == len_updated_feed_list:
        return f"Nothing removed from the list" 
    else:
        return f"RSS feed list updated removing {len_original_feed_list - len(rss_feeds)} feeds from the list"
    
@tool(return_direct=True)
def get_latest_news(cat):
    """
        Get latest news from the rss feed list. 
        User may say: 
            - "Give me the latest news from my list"
            - "Fetch me the freshest headlines from my RSS feed, please."
            - "Show me the most up-to-date stories from my personalized RSS feed."
            - "Can you serve up the latest news morsels from my RSS feed?"
            - "I'm curious, what are the latest tidbits from my RSS feed?"
            - "Surprise me with the newest gems from my RSS feed."
            - or similar even in other languages
    """
    rss_feeds = get_rss_feeds()
    rss_feed_urls = [feed["url"] for feed in rss_feeds]
    rss_feed_news = [fetch_rss_data(url) for url in rss_feed_urls]
    return rss_feed_news