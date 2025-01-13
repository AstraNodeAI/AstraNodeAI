from tweepy import Client
from textblob import TextBlob
import logging
from config import TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET

class EngagementMonitor:
    def __init__(self):
        self.client = Client(
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_SECRET
        )
        self.logger = logging.getLogger(__name__)

    def get_engagement_metrics(self, tweet_id):
        """
        Fetch engagement metrics (likes, retweets, replies) for a tweet.
        """
        try:
            tweet = self.client.get_tweet(tweet_id, tweet_fields=["public_metrics"])
            return tweet.data['public_metrics']
        except Exception as e:
            self.logger.error(f"Error fetching engagement metrics: {e}")
            return None

    def analyze_sentiment(self, text):
        """
        Perform sentiment analysis on a text.
        """
        analysis = TextBlob(text)
        return analysis.sentiment.polarity