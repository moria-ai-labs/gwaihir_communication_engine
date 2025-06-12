import tweepy
from . import config # Use relative import if config.py is in the same directory

def get_twitter_client():
    """Initializes and returns a Tweepy API client."""
    if not all([config.X_API_KEY, config.X_API_SECRET_KEY, config.X_ACCESS_TOKEN, config.X_ACCESS_TOKEN_SECRET]):
        raise ValueError("Twitter API credentials are not fully configured. "
                         "Please check your .env file or environment variables.")

    # Authenticate to Twitter V1.1 API (for media upload if needed later)
    # auth = tweepy.OAuth1UserHandler(
    #    config.X_API_KEY, config.X_API_SECRET_KEY,
    #    config.X_ACCESS_TOKEN, config.X_ACCESS_TOKEN_SECRET
    # )
    # api_v1 = tweepy.API(auth)

    # Using Tweepy's Client for V2 API (preferred for most text-based operations)
    client = tweepy.Client(
        consumer_key=config.X_API_KEY,
        consumer_secret=config.X_API_SECRET_KEY,
        access_token=config.X_ACCESS_TOKEN,
        access_token_secret=config.X_ACCESS_TOKEN_SECRET
    )
    return client # , api_v1 (if using both v1 and v2)

def post_tweet(text: str):
    """
    Posts a tweet to Twitter.
    Args:
        text (str): The text content of the tweet. Max 280 characters.
    Returns:
        The response from the Twitter API, or None if an error occurs.
    """
    if not text:
        print("Error: Tweet text cannot be empty.")
        return None
    if len(text) > 280:
        print(f"Error: Tweet text is too long ({len(text)} characters). Maximum is 280.")
        # Consider truncating or raising an error
        # text = text[:280]
        return None

    try:
        client = get_twitter_client()
        response = client.create_tweet(text=text)
        print(f"Tweet posted successfully! Tweet ID: {response.data['id']}")
        return response
    except tweepy.TweepyException as e:
        print(f"Error posting tweet: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == '__main__':
    # This section is for testing purposes.
    # It will only run if the script is executed directly.
    # print("Attempting to post a test tweet...")
    # To use this test:
    # 1. Make sure your .env file has the correct Twitter API keys.
    # 2. Uncomment the lines below.
    # 3. Run this file directly: python twitter_bot/twitter_client.py

    # Ensure config is loaded if running standalone for testing
    # import sys
    # import os
    # # Add parent directory to sys.path to allow direct execution and finding config
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # parent_dir = os.path.dirname(current_dir)
    # if parent_dir not in sys.path:
    #    sys.path.insert(0, parent_dir)
    # from twitter_bot import config # now this should work

    # if config.X_API_KEY: # Check if keys are loaded
    #    test_tweet_text = "Hello from my Tweepy bot! This is a test tweet. #Python #TwitterBot"
    #    post_tweet(test_tweet_text)
    # else:
    #    print("Skipping test tweet: API keys not found in config.")
    pass
