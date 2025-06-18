import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any, List, Optional # For type hinting mock returns
import datetime # For created_at fields

# Assuming twitter_client.py is in the parent directory of 'tests'
# Adjust import if your structure is different or you have specific path setups
# For example, if 'twitter_bot' is in PYTHONPATH or tests are run from project root.
# This import assumes tests might be run as 'python -m unittest discover' from project root.
from twitter_bot.twitter_client import get_twitter_user_info
# from twitter_bot import config # To potentially mock config values if needed, though not directly for this test

# Import TweepyException for error simulation if not already available via twitter_client
try:
    from tweepy import TweepyException
except ImportError:
    # Define a dummy exception if tweepy is not installed in the test environment
    # (though it should be if it's a dependency of the tested code)
    class TweepyException(Exception):
        pass

class TestTwitterClient(unittest.TestCase):

    @patch('twitter_bot.twitter_client.get_twitter_client')
    def test_get_twitter_user_info_success(self, mock_get_twitter_client):
        # --- Mocking setup ---
        mock_client = MagicMock()
        mock_get_twitter_client.return_value = mock_client

        # Mock data for get_user response
        mock_user_data = MagicMock()
        mock_user_data.id = "12345"
        mock_user_data.name = "Test User"
        mock_user_data.username = "testuser"
        # Use datetime objects for created_at as Tweepy would return them
        mock_user_data.created_at = datetime.datetime.fromisoformat("2023-01-01T00:00:00+00:00")
        mock_user_data.description = "Test description"
        mock_user_data.location = "Test location"
        mock_user_data.profile_image_url = "http://example.com/profile.jpg"
        mock_user_data.url = "http://example.com"
        mock_user_data.verified = False
        mock_user_data.public_metrics = {
            'followers_count': 100,
            'following_count': 50,
            'tweet_count': 200,
            'listed_count': 10
        }
        mock_client.get_user.return_value = MagicMock(data=mock_user_data)

        # Mock data for get_users_tweets response
        mock_tweet1_data = MagicMock()
        mock_tweet1_data.id = "t1"
        mock_tweet1_data.text = "Hello world! #test"
        mock_tweet1_data.created_at = datetime.datetime.fromisoformat("2023-10-26T10:00:00+00:00")
        mock_tweet1_data.public_metrics = {'like_count': 10, 'retweet_count': 2, 'reply_count': 1, 'quote_count': 0}
        mock_tweet1_data.attachments = {'media_keys': ['mk1']}

        mock_tweet2_data = MagicMock()
        mock_tweet2_data.id = "t2"
        mock_tweet2_data.text = "Another tweet, no media."
        mock_tweet2_data.created_at = datetime.datetime.fromisoformat("2023-10-27T11:00:00+00:00")
        mock_tweet2_data.public_metrics = {'like_count': 5, 'retweet_count': 1, 'reply_count': 0, 'quote_count': 0}
        mock_tweet2_data.attachments = None

        mock_tweets_response = MagicMock()
        mock_tweets_response.data = [mock_tweet1_data, mock_tweet2_data]

        # Mock media includes for the tweet with media
        mock_media1 = MagicMock()
        mock_media1.media_key = "mk1"
        mock_media1.type = "photo"
        mock_media1.url = "http://example.com/image.jpg"
        mock_media1.preview_image_url = "http://example.com/preview_image.jpg" # Fallback if url is None

        mock_tweets_response.includes = {'media': [mock_media1]}
        mock_client.get_users_tweets.return_value = mock_tweets_response

        # --- Call the function ---
        result = get_twitter_user_info("testuser")

        # --- Assertions ---
        self.assertIsNotNone(result)
        self.assertEqual(result['username'], "testuser")
        self.assertEqual(result['followers_count'], 100)
        self.assertEqual(result['created_at'], "2023-01-01T00:00:00+00:00") # Check ISO format string
        self.assertIn('recent_tweets', result)
        self.assertEqual(len(result['recent_tweets']), 2)

        first_tweet = result['recent_tweets'][0]
        self.assertEqual(first_tweet['text'], "Hello world! #test")
        self.assertEqual(first_tweet['created_at'], "2023-10-26T10:00:00+00:00")
        self.assertEqual(first_tweet['like_count'], 10)
        self.assertIn('image_urls', first_tweet)
        self.assertEqual(len(first_tweet['image_urls']), 1)
        self.assertEqual(first_tweet['image_urls'][0], "http://example.com/image.jpg")
        self.assertIn('mk1', first_tweet['media_keys'])

        second_tweet = result['recent_tweets'][1]
        self.assertEqual(second_tweet['text'], "Another tweet, no media.")
        self.assertEqual(len(second_tweet['image_urls']), 0)

        mock_client.get_user.assert_called_once_with(
            username="testuser",
            user_fields=['public_metrics', 'id', 'name', 'username', 'created_at', 'description', 'location', 'profile_image_url', 'url', 'verified']
        )
        mock_client.get_users_tweets.assert_called_once_with(
            id="12345",
            max_results=5,
            tweet_fields=['created_at', 'public_metrics', 'text', 'attachments'],
            expansions=['attachments.media_keys']
        )

    @patch('twitter_bot.twitter_client.get_twitter_client')
    def test_get_twitter_user_info_user_not_found(self, mock_get_twitter_client):
        mock_client = MagicMock()
        mock_get_twitter_client.return_value = mock_client
        mock_client.get_user.return_value = MagicMock(data=None)

        result = get_twitter_user_info("nonexistentuser")

        self.assertIsNone(result)
        mock_client.get_user.assert_called_once_with(
            username="nonexistentuser",
            user_fields=['public_metrics', 'id', 'name', 'username', 'created_at', 'description', 'location', 'profile_image_url', 'url', 'verified']
        )
        mock_client.get_users_tweets.assert_not_called()

    @patch('twitter_bot.twitter_client.get_twitter_client')
    def test_get_twitter_user_info_api_error_on_get_user(self, mock_get_twitter_client):
        mock_client = MagicMock()
        mock_get_twitter_client.return_value = mock_client
        mock_client.get_user.side_effect = TweepyException("API Error")

        result = get_twitter_user_info("testuser_api_error")
        self.assertIsNone(result)
        mock_client.get_users_tweets.assert_not_called()

    @patch('twitter_bot.twitter_client.get_twitter_client')
    def test_get_twitter_user_info_api_error_on_get_tweets(self, mock_get_twitter_client):
        mock_client = MagicMock()
        mock_get_twitter_client.return_value = mock_client

        mock_user_data = MagicMock(id="12345", name="Test User", username="testuser_tweet_error", public_metrics={'followers_count': 100}, created_at=datetime.datetime.now(), description=None, location=None, profile_image_url=None, url=None, verified=False) # simplified
        mock_client.get_user.return_value = MagicMock(data=mock_user_data)
        mock_client.get_users_tweets.side_effect = TweepyException("Failed to fetch tweets")

        result = get_twitter_user_info("testuser_tweet_error")
        self.assertIsNone(result)

    @patch('twitter_bot.twitter_client.get_twitter_client')
    def test_get_twitter_user_info_no_tweets_found(self, mock_get_twitter_client):
        mock_client = MagicMock()
        mock_get_twitter_client.return_value = mock_client

        mock_user_data = MagicMock(id="67890", name="No Tweet User", username="notweetuser", public_metrics={'followers_count': 10, 'tweet_count':0}, created_at=datetime.datetime.now(), description=None, location=None, profile_image_url=None, url=None, verified=False) # simplified
        mock_client.get_user.return_value = MagicMock(data=mock_user_data)

        mock_tweets_response = MagicMock()
        mock_tweets_response.data = []
        mock_tweets_response.includes = None
        mock_client.get_users_tweets.return_value = mock_tweets_response

        result = get_twitter_user_info("notweetuser")

        self.assertIsNotNone(result)
        self.assertEqual(result['username'], "notweetuser")
        self.assertEqual(len(result['recent_tweets']), 0)
        # Ensure tweet_media_includes is not present or empty if no tweets or no media
        self.assertNotIn("tweet_media_includes", result)


    @patch('twitter_bot.twitter_client.get_twitter_client')
    def test_get_twitter_user_info_tweet_with_no_image_in_media(self, mock_get_twitter_client):
        mock_client = MagicMock()
        mock_get_twitter_client.return_value = mock_client

        mock_user_data = MagicMock(id="123", username="user_video_tweet", name="User Video Tweet", public_metrics={}, created_at=datetime.datetime.now(), description=None, location=None, profile_image_url=None, url=None, verified=False)
        mock_client.get_user.return_value = MagicMock(data=mock_user_data)

        mock_tweet_video = MagicMock(id="tv1", text="Tweet with video", created_at=datetime.datetime.now(), public_metrics={}, attachments={'media_keys': ['mkv1']})
        mock_tweets_response = MagicMock(data=[mock_tweet_video])

        mock_media_video = MagicMock(media_key="mkv1", type="video") # No 'url' or 'preview_image_url' needed for this test of type
        mock_tweets_response.includes = {'media': [mock_media_video]}
        mock_client.get_users_tweets.return_value = mock_tweets_response

        result = get_twitter_user_info("user_video_tweet")

        self.assertIsNotNone(result)
        self.assertEqual(len(result['recent_tweets']), 1)
        tweet_result = result['recent_tweets'][0]
        self.assertEqual(len(tweet_result['image_urls']), 0) # Expect no image URLs

if __name__ == '__main__':
    unittest.main()
