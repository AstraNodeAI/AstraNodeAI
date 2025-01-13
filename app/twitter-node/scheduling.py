import schedule
import time
from tweepy import Client
import logging
from config import TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET

class TweetScheduler:
    def __init__(self):
        self.client = Client(
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_SECRET
        )
        self.logger = logging.getLogger(__name__)

    def schedule_tweet(self, tweet, time_str):
        """
        Schedule a tweet to be posted at a specific time.
        """
        schedule.every().day.at(time_str).do(self.post_tweet, tweet)

    def post_tweet(self, tweet):
        """
        Post a tweet to Twitter.
        """
        try:
            response = self.client.create_tweet(text=tweet)
            self.logger.info(f"Tweet posted: {response.data['text']}")
        except Exception as e:
            self.logger.error(f"Error posting tweet: {e}")

    def run_scheduler(self):
        """
        Run the scheduler to check for pending tweets.
        """
        while True:
            schedule.run_pending()
            time.sleep(1)