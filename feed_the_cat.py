import time
import json
import os

import logging
from cat.mad_hatter.decorators import hook, tool
from datetime import datetime, timedelta

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
def get_feed_list(tool_input, cat):
    """
        Shows all the items in the rss feed list. 
        User may say: 
            - "Show me my RSS feed list"
            - "What's inside my RSS feed list"
            -  or similar even in other languages
    """
    rss_feeds = get_rss_feeds()
    return str(rss_feeds)

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
        return "Nothing removed from the list" 
    else:
        return f"RSS feed list updated removing {len_original_feed_list - len(rss_feeds)} feeds from the list"
    
@tool(return_direct=True)
def get_latest_news(tool_input, cat):
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

    settings_json_path = os.path.join(os.path.dirname(__file__), "settings.json")
    if os.stat(settings_json_path).st_size == 0:
        with open(settings_json_path, "w") as fp:
            data = {"last_update": str(datetime.now())}
            json.dump(fp=fp, obj=data)

    rss_feeds = get_rss_feeds()
    
    with open(settings_json_path) as fp:
        data = json.load(fp)
        last_update = data.get("last_update", (datetime.now() - timedelta(days=-1)).strftime("%Y-%m-%d %H:%M:%S.%f"))


    rss_feed_urls = [feed["url"] for feed in rss_feeds]
    rss_feed_news = [fetch_rss_data(url) for url in rss_feed_urls]
    output = " \n".join(f"{entry.title}: {entry.link}" for sublist in rss_feed_news for entry in sublist if datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z").strftime("%Y-%m-%d %H:%M:%S.%f") >= last_update)
    
    if len(output) > 0:
        output_llm = cat.llm(f"""
                            Can you please convert this string {output} in a bullet point.
                            Each point must have the following structure: article title, article link.
                            The answer must begn with "Stay in the know with the freshest news from your feed"
                            """)
    else:
        output_llm = cat.llm("Write a sentence meaning that there are no news at the moment")
    
    with open(settings_json_path, "w") as fp:
        data = {"last_update": str(datetime.now())}
        json.dump(fp=fp, obj=data)
    return output_llm