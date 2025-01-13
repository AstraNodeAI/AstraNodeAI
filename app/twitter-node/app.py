from flask import Flask, request, jsonify
from content_generation import ContentGenerator
from scheduling import TweetScheduler
from monitoring import EngagementMonitor
from interaction import InteractionManager
import threading
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize modules
content_generator = ContentGenerator()
tweet_scheduler = TweetScheduler()
engagement_monitor = EngagementMonitor()
interaction_manager = InteractionManager()

# Configure logging
logging.basicConfig(level=logging.INFO)

def start_scheduler():
    """
    Start the tweet scheduler in a separate thread.
    """
    scheduler_thread = threading.Thread(target=tweet_scheduler.run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

@app.route("/generate_tweet", methods=["POST"])
def generate_tweet():
    data = request.json
    if not data or "prompt" not in data:
        return jsonify({"error": "Prompt is required"}), 400

    prompt = data.get("prompt")
    hashtags = data.get("hashtags", [])
    tweet = content_generator.generate_tweet(prompt)
    if not tweet:
        return jsonify({"error": "Failed to generate tweet"}), 500

    tweet_with_hashtags = content_generator.add_hashtags(tweet, hashtags)
    return jsonify({"tweet": tweet_with_hashtags})

@app.route("/schedule_tweet", methods=["POST"])
def schedule_tweet():
    data = request.json
    if not data or "tweet" not in data or "time" not in data:
        return jsonify({"error": "Tweet and time are required"}), 400

    tweet = data.get("tweet")
    time_str = data.get("time")
    tweet_scheduler.schedule_tweet(tweet, time_str)
    return jsonify({"message": "Tweet scheduled successfully"})

@app.route("/get_engagement", methods=["GET"])
def get_engagement():
    tweet_id = request.args.get("tweet_id")
    if not tweet_id:
        return jsonify({"error": "Tweet ID is required"}), 400

    metrics = engagement_monitor.get_engagement_metrics(tweet_id)
    if not metrics:
        return jsonify({"error": "Failed to fetch engagement metrics"}), 500

    return jsonify(metrics)

@app.route("/reply_to_mention", methods=["POST"])
def reply_to_mention():
    data = request.json
    if not data or "mention_id" not in data or "reply_text" not in data:
        return jsonify({"error": "Mention ID and reply text are required"}), 400

    mention_id = data.get("mention_id")
    reply_text = data.get("reply_text")
    interaction_manager.reply_to_mention(mention_id, reply_text)
    return jsonify({"message": "Reply sent successfully"})

if __name__ == "__main__":
    start_scheduler()
    app.run(debug=True)