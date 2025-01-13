from transformers import pipeline
import logging

class ContentGenerator:
    def __init__(self, model_name="gpt2"):
        self.generator = pipeline("text-generation", model=model_name)
        self.logger = logging.getLogger(__name__)

    def generate_tweet(self, prompt, max_length=280):
        """
        Generate a tweet using a pre-trained language model.
        """
        try:
            generated_text = self.generator(prompt, max_length=max_length, num_return_sequences=1)
            return generated_text[0]['generated_text']
        except Exception as e:
            self.logger.error(f"Error generating tweet: {e}")
            return None

    def add_hashtags(self, tweet, hashtags):
        """
        Append trending hashtags to a tweet.
        """
        return f"{tweet} {' '.join(hashtags)}"