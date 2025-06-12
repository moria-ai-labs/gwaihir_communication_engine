# Using absolute imports for clarity, assuming 'twitter_bot' is the root package
# If running as a script directly in the 'twitter_bot' folder, relative imports might be needed
# depending on PYTHONPATH setup or how the script is invoked.
# For package structure, it's often better to run as 'python -m twitter_bot.main' from parent dir.

try:
    from . import twitter_client
    from . import content_manager
    from . import config # To ensure config is loaded, though not directly used here often
except ImportError:
    # Fallback for direct execution (e.g., python main.py from within twitter_bot dir)
    # This is less ideal for package structures but common for simple scripts.
    import twitter_client
    import content_manager
    import config

def post_latest_article():
    """
    Fetches the latest articles from RSS feeds and posts the first one to Twitter.
    """
    print("Attempting to post the latest article...")

    # 1. Fetch articles
    #    For now, using default RSS feeds.
    #    This could be expanded to take feed URLs from config or other sources.
    articles = content_manager.fetch_rss_feeds()

    if not articles:
        print("No articles fetched. Nothing to post.")
        return

    # 2. Select an article
    #    For simplicity, let's pick the first article.
    #    More sophisticated selection logic can be added later (e.g., random, based on keywords).
    article_to_post = articles[0]
    title = article_to_post.get("title")
    link = article_to_post.get("link")

    if not title or not link:
        print("Selected article is missing a title or link. Skipping.")
        return

    # 3. Construct the tweet
    #    Basic format. Can be made more engaging.
    #    Consider character limits. A simple way is to truncate the title if too long.
    #    Max tweet length is 280. Link takes up t.co length (around 23 chars).
    #    "News: ... [link]" leaves about 280 - 6 - 23 = 251 chars for title.
    max_title_len = 250 # A bit of buffer
    if len(title) > max_title_len:
        title = title[:max_title_len-3] + "..."

    tweet_text = f"News: {title} {link}"

    # An alternative for more topics:
    # tweet_text = f"Check out this article on {topic_keyword}: {title} {link} #Data #AI"

    print(f"Prepared tweet: {tweet_text}")

    # 4. Post the tweet
    #    This requires API keys to be correctly set in the .env file.
    try:
        twitter_client.post_tweet(tweet_text)
        print("Tweet posting process initiated from main.py.")
    except Exception as e:
        print(f"An error occurred while trying to post tweet from main.py: {e}")

if __name__ == '__main__':
    print("Running twitter_bot main.py...")
    # Ensure API keys are loaded by importing config first
    # (already done by the import at the top if relative imports work,
    # or by the fallback direct import)
    if not config.X_API_KEY: # A simple check
        print("WARNING: Twitter API keys not found in config. Tweet posting will likely fail.")
        print("Please ensure your .env file is set up correctly in the 'twitter_bot' directory.")

    post_latest_article()
    print("twitter_bot main.py finished.")
