import feedparser
import pandas as pd
from datetime import datetime
import time

# 1. DEFINE YOUR SOURCES
# We want a mix of tech and general news to test our categorization later.
RSS_FEEDS = {
    # Tech & Business
    "The Verge": "https://www.theverge.com/rss/index.xml",
    "TechCrunch": "https://techcrunch.com/feed/",
    "Ars Technica": "https://feeds.arstechnica.com/arstechnica/index",
    "Engadget": "https://www.engadget.com/rss.xml",
    "Wired": "https://www.wired.com/feed/rss",
    "VentureBeat": "http://feeds.feedburner.com/venturebeat/SZYF",
    "BBC Tech": "http://feeds.bbci.co.uk/news/technology/rss.xml",
    "NYT Tech": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "CNBC Tech": "https://www.cnbc.com/id/19854910/device/rss/rss.html",
    
    # AI Specific (Good for finding duplicates)
    "OpenAI Blog": "https://openai.com/blog/rss.xml",
    "MIT AI News": "https://news.mit.edu/rss/topic/artificial-intelligence2",
    "Google AI": "http://googleaiblog.blogspot.com/atom.xml",
    
    # Science (To test categorization)
    "NASA": "https://www.nasa.gov/rss/dyn/breaking_news.rss",
    "Space.com": "https://www.space.com/feeds/all",
    "Science Daily": "https://www.sciencedaily.com/rss/top/science.xml"
}

def fetch_articles(feeds_dict):
    """
    Fetches articles from a dictionary of RSS feeds.
    Returns a list of dictionaries.
    """
    articles = []
    
    print(f"--- Starting Scraping Job at {datetime.now()} ---")
    
    for source, url in feeds_dict.items():
        print(f"Fetching {source}...")
        try:
            # Parse the feed
            feed = feedparser.parse(url)
            
            # Check if it worked (status 200 means OK)
            # Note: feedparser doesn't always return status, so we check entries too.
            if not feed.entries:
                print(f"⚠️ Warning: No entries found for {source}")
                continue

            # Loop through each article in the feed
            for entry in feed.entries:
                article = {
                    "source": source,
                    "title": entry.title,
                    "link": entry.link,
                    # Some feeds use 'published', others 'updated'. We try both.
                    "published": entry.get("published", entry.get("updated", "N/A")),
                    # Summary is often where the "clickbait" reveals itself
                    "summary": entry.get("summary", entry.get("description", "")),
                    "scraped_at": datetime.now().isoformat()
                }
                articles.append(article)
                
        except Exception as e:
            print(f"❌ Error fetching {source}: {e}")
            
    print(f"--- Job Complete. Fetched {len(articles)} articles. ---")
    return articles

# 3. RUN THE SCRAPER
if __name__ == "__main__":
    # Fetch the data
    raw_data = fetch_articles(RSS_FEEDS)
    
    # Convert to a Pandas DataFrame (Excel-like table)
    df = pd.DataFrame(raw_data)
    
    # Basic Cleaning: Remove HTML tags from summaries (optional but recommended)
    # This regex removes <p>, <a>, etc. to leave just text
    df['summary'] = df['summary'].str.replace(r'<[^>]*>', '', regex=True)
    
    # Preview the data
    print("\nHead of the DataFrame:")
    print(df.head())
    
    # 4. SAVE IT (The "Database" for now)
    # We save to CSV so we don't have to scrape every time we test the next step.
    filename = f"news_data_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False)
    print(f"\nSaved data to {filename}")
