# /// script
# dependencies =[
#     "pandas",
#     "feedparser",
# ]
# ///

import feedparser
import pandas as pd
from pathlib import Path


RSS_FEEDS = {
    'Yahoo Finance': 'https://finance.yahoo.com/news/rssindex',
    'Hacker News': 'https://news.ycombinator.com/rss',
    'Wall Street Journal': 'https://feeds.a.dj.com/rss/RSSMarketsMain.xml',
    'CNBC': 'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839069'
}

RSS_FEEDS_AI = {
    "Machine Learning Mastery" : "https://machinelearningmastery.com/blog/feed/",
    "BAIR Blog" : "https://bair.berkeley.edu/blog/feed.xml",
    "MIT News" : "http://news.mit.edu/rss/topic/artificial-intelligence2",
    "DeepMind" : "https://deepmind.com/blog/feed/basic/"
}


def flatten_entry(source, entry, all_keys):
    flat_entry = {}
    flat_entry['source'] = source

    for key in all_keys:
        value = entry.get(key, None)

        if isinstance(value, dict):
            flat_entry.update({f"{key}_{subkey}": subvalue for subkey, subvalue in value.items()})
        
        elif isinstance(value, list):
            if value and isinstance(value[0], dict):
                for i, item in enumerate(value):
                    flat_entry.update({f"{key}_{i}_{subkey}":subvalue for subkey, subvalue in item.items()})
            else:
                flat_entry[key] = ", ".join(str(item) for item in value)
        
        else:
            flat_entry[key] = value
    
    return flat_entry



def process_feed(feed_source, feed_url):
    feed = feedparser.parse(feed_url)
    
    all_keys = set()
    for entry in feed.entries:
        all_keys.update(entry.keys())

    data = [flatten_entry(feed_source, entry, all_keys) for entry in feed.entries]
    return data


def feed_to_df():
    all_data = []
    for feed_source, feed_url in RSS_FEEDS.items():
        all_data.extend(process_feed(feed_source, feed_url))

    df = pd.DataFrame(all_data)
    return df
    


if __name__ == "__main__":
    path = Path("data/history.csv")
    daily_dataframe = feed_to_df()
    if not path.exists():
        daily_dataframe.to_csv('data/history.csv', index=False)
    
    existing_dataframe = pd.read_csv('data/history.csv')
    daily_dataframe = pd.concat([existing_dataframe, daily_dataframe]).drop_duplicates(subset=['published'], keep='last')
    daily_dataframe.to_csv(path,sep='\t', index=False)


