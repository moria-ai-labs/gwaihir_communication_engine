import feedparser

# Placeholder RSS feeds - these should be related to data, AI, etc.
# The user should replace these with relevant sources.
DEFAULT_RSS_FEEDS = [
    "http://rss. основных новостей технологий Wired.com", # Example: Wired Technology News
    "https://www.artificialintelligence-news.com/feed/",
    "https://feeds.feedburner.com/DataScienceCentral",
    # Add more relevant feeds here
]

def fetch_rss_feeds(feed_urls=None):
    """
    Fetches and parses articles from a list of RSS feed URLs.

    Args:
        feed_urls (list, optional): A list of RSS feed URLs to fetch.
                                    Defaults to DEFAULT_RSS_FEEDS.

    Returns:
        list: A list of dictionaries, where each dictionary contains
              'title' and 'link' of an article. Returns empty if error.
    """
    if feed_urls is None:
        feed_urls = DEFAULT_RSS_FEEDS

    articles = []
    if not feed_urls:
        print("No RSS feed URLs provided.")
        return articles

    for url in feed_urls:
        try:
            print(f"Fetching feed: {url}")
            feed = feedparser.parse(url)

            # Check for errors in parsing
            if feed.bozo:
                # Bozo bit is set if the feed is not well-formed XML
                # feed.bozo_exception often contains more details
                print(f"Warning: Feed at {url} might be ill-formed. Error: {feed.bozo_exception}")
                # Continue to try and extract entries if possible, or skip
                # For now, we'll try to process entries even if bozo is set

            if not feed.entries:
                print(f"No entries found in feed: {url}")
                continue

            for entry in feed.entries:
                title = entry.get("title")
                link = entry.get("link")
                if title and link:
                    articles.append({"title": title, "link": link})
                else:
                    # Log if an entry is missing title or link
                    print(f"Skipping entry in {url} due to missing title or link: {entry}")

            print(f"Found {len(feed.entries)} entries in {url}, successfully processed {len(articles)} articles from this feed so far.")

        except Exception as e:
            print(f"Error fetching or parsing RSS feed {url}: {e}")
            # Optionally, decide if one failing feed should stop all, or just skip
            continue

    return articles

if __name__ == '__main__':
    # This section is for testing purposes.
    # It will only run if the script is executed directly.
    print("Fetching articles from default RSS feeds...")
    fetched_articles = fetch_rss_feeds()
    if fetched_articles:
        print(f"Successfully fetched {len(fetched_articles)} articles:")
        for i, article in enumerate(fetched_articles[:5]): # Print first 5
            print(f"{i+1}. {article['title']} - {article['link']}")
    else:
        print("No articles fetched.")

    # Example with a custom feed list
    # custom_feeds = ["http://rss. основных новостей технологий Wired.com"] # Replace with a valid feed for testing
    # print("\nFetching articles from a custom RSS feed list...")
    # custom_articles = fetch_rss_feeds(custom_feeds)
    # if custom_articles:
    #    print(f"Successfully fetched {len(custom_articles)} articles:")
    #    for i, article in enumerate(custom_articles[:5]):
    #        print(f"{i+1}. {article['title']} - {article['link']}")
    # else:
    #    print("No articles fetched from custom list.")
