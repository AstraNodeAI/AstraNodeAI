from tweepy import Client
import logging
from config import TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET

class InteractionManager:
    def __init__(self):
        self.client = Client(
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_SECRET
        )
        self.logger = logging.getLogger(__name__)

    def reply_to_mention(self, mention_id, reply_text):
        """
        Reply to a mention or tweet.
        """
        try:
            response = self.client.create_tweet(text=reply_text, in_reply_to_tweet_id=mention_id)
            self.logger.info(f"Replied to mention: {response.data['text']}")
        except Exception as e:
            self.logger.error(f"Error replying to mention: {e}")

    def follow_user(self, user_id):
        """
        Follow a user based on AI recommendations.
        """
        try:
            self.client.follow_user(user_id)
            self.logger.info(f"Followed user: {user_id}")
        except Exception as e:
            self.logger.error(f"Error following user: {e}")