import tweepy
from typing import Optional, Dict, Any, List # Added type hints
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

def get_twitter_user_info(username: str) -> Optional[Dict[str, Any]]:
    """
    Fetches public information for a given X/Twitter username.

    Args:
        username (str): The X/Twitter handle (without '@').

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing user and tweet information
        if the user is found and data is successfully retrieved. Returns None if
        the user is not found, or if there's an API error.

        The returned dictionary has the following structure:
        {
            "id": str,                            # User ID
            "name": str,                          # Display name
            "username": str,                      # Screen name / handle
            "created_at": str,                    # User account creation date (ISO format)
            "description": str,                   # User profile description
            "location": Optional[str],            # User profile location (if provided)
            "profile_image_url": Optional[str],   # URL of profile image
            "url": Optional[str],                 # URL listed in user profile (if any)
            "verified": bool,                     # True if user is verified
            "followers_count": int,               # Number of followers
            "following_count": int,               # Number of users they are following
            "tweet_count": int,                   # Total number of tweets posted
            "listed_count": int,                  # Number of lists the user is on
            "recent_tweets": [
                {
                    "id": str,                    # Tweet ID
                    "text": str,                  # Tweet text
                    "created_at": str,            # Tweet creation date (ISO format)
                    "like_count": int,
                    "retweet_count": int,
                    "reply_count": int,
                    "quote_count": int,
                    "media_keys": List[str],      # Keys for media attachments (if any)
                    "image_urls": List[str]       # URLs of images attached to the tweet
                },
                # ... more tweets
            ]
        }
    """
    print(f"Attempting to fetch info for {username}")
    try:
        client = get_twitter_client()
        response = client.get_user(
            username=username,
            user_fields=['public_metrics', 'id', 'name', 'username', 'created_at', 'description', 'location', 'profile_image_url', 'url', 'verified']
        )

        if response.data:
            user = response.data
            user_info = {
                "id": user.id,
                "name": user.name,
                "username": user.username,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "description": user.description,
                "location": user.location,
                "profile_image_url": user.profile_image_url,
                "url": user.url,
                "verified": user.verified,
                "followers_count": user.public_metrics['followers_count'] if user.public_metrics else 0,
                "following_count": user.public_metrics['following_count'] if user.public_metrics else 0,
                "tweet_count": user.public_metrics['tweet_count'] if user.public_metrics else 0,
                "listed_count": user.public_metrics['listed_count'] if user.public_metrics else 0
            }
            # For now, just print and return this basic info
            # print(f"User info for {username}: {user_info}") # Original print
            # return user_info # Original return

            # Now fetch recent tweets
            user_id = user_info["id"]
            tweets_response = client.get_users_tweets(
                id=user_id,
                max_results=5,
                tweet_fields=['created_at', 'public_metrics', 'text', 'attachments'],
                expansions=['attachments.media_keys']
            )

            recent_tweets_data = []
            if tweets_response.data:
                for tweet in tweets_response.data:
                    tweet_details = {
                        "id": tweet.id,
                        "text": tweet.text,
                        "created_at": tweet.created_at.isoformat(),
                        "like_count": tweet.public_metrics.get('like_count', 0),
                        "retweet_count": tweet.public_metrics.get('retweet_count', 0),
                        "reply_count": tweet.public_metrics.get('reply_count', 0),
                        "quote_count": tweet.public_metrics.get('quote_count', 0),
                        "media_keys": tweet.attachments['media_keys'] if tweet.attachments and 'media_keys' in tweet.attachments else []
                    }
                    recent_tweets_data.append(tweet_details)

            user_info["recent_tweets"] = recent_tweets_data

            # Store media objects if available in 'includes'
            if tweets_response.includes and 'media' in tweets_response.includes:
                user_info["tweet_media_includes"] = tweets_response.includes['media']
            else:
                user_info["tweet_media_includes"] = []

            # Process media includes to get image URLs
            media_map = {}
            if user_info["tweet_media_includes"]:
                for media_item in user_info["tweet_media_includes"]:
                    if media_item.type == 'photo' and media_item.media_key:
                        media_map[media_item.media_key] = media_item.url if media_item.url else media_item.preview_image_url

            for tweet_details in user_info["recent_tweets"]:
                image_urls = []
                if "media_keys" in tweet_details and tweet_details["media_keys"]:
                    for key in tweet_details["media_keys"]:
                        if key in media_map:
                            image_urls.append(media_map[key])
                tweet_details["image_urls"] = image_urls
                # Optionally remove media_keys if they are no longer needed directly in the tweet object
                # del tweet_details["media_keys"]

            # Remove temporary media includes field
            if "tweet_media_includes" in user_info:
                del user_info["tweet_media_includes"]

            print(f"User info for {username} (with tweets and image URLs): {user_info}")
            return user_info
        else:
            print(f"User {username} not found.")
            return None
    except tweepy.TweepyException as e:
        print(f"Tweepy API error fetching data for user {username}: {e}") # Modified error message slightly
        return None
    except Exception as e:
        print(f"Unexpected error fetching data for user {username}: {e}") # Modified error message slightly
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
