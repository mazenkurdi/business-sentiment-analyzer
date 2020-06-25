import os
import re
from dateutil.parser import parse
from .twitter_api import TwitterApi
from .user_display import UserDisplay
from .cache import Cache
from textblob import TextBlob

dirname = os.path.dirname(__file__)
cached_data_path = os.path.join(dirname, "cache/raw_data")
cached_results_path = os.path.join(dirname, "cache/cached_results")


class BusinessSentimentAnalyzer:
    def __init__(self, twitter_credentials):
        self.twitter_api = TwitterApi(
            twitter_credentials['consumer_key'],
            twitter_credentials['consumer_secret'],
            twitter_credentials['access_token'],
            twitter_credentials['access_token_secret'],
        )
        self.user_display = UserDisplay()
        self.cache = Cache()

    def analyze(self, query, opts):
        query = query.lower()
        refresh_cache = opts["refresh_cache"]
        print_results = opts["print_results"]
        with_time_context = opts["with_time_context"]

        cache_path_base = cached_results_path
        if with_time_context:
            cache_path_base += "/with_time"

        results = None
        if not refresh_cache:
            results = self.check_cached_results(f"{cache_path_base}/{query}.txt")

        if not results:
            tweets = self.load_tweets(query, refresh_cache)

            if with_time_context:
                results = self.analyze_over_time(tweets)
            else:
                results = [self.analyze_tweets(tweets)]

            self.cache.cache(f"{cache_path_base}/{query}.txt", results)

        if print_results:
            self.user_display.display(query, results)

        return results

    def analyze_over_time(self, tweets):
        tweets_by_date = self.segment_by_date(tweets)
        results = []

        for k, v in tweets_by_date.items():
            result = self.analyze_tweets(v)
            result['date'] = k
            results.append(result)

        return results

    def analyze_tweets(self, tweets):
        polarity_sum = 0
        subjectivity_sum = 0
        number_of_positive_tweets = 0
        number_of_neutral_tweets = 0
        number_of_negative_tweets = 0

        for tweet in tweets:
            analysis = self.analyze_sentiment(tweet['text'])

            if analysis.polarity > 0:
                number_of_positive_tweets += 1
            elif analysis.polarity == 0:
                number_of_neutral_tweets += 1
            else:
                number_of_negative_tweets += 1

            polarity_sum += analysis.polarity
            subjectivity_sum += analysis.subjectivity

        return {
            "date": None,
            "number_of_tweets": len(tweets),
            "number_of_positive_tweets": number_of_positive_tweets,
            "number_of_neutral_tweets": number_of_neutral_tweets,
            "number_of_negative_tweets": number_of_negative_tweets,
            "average_polarity": polarity_sum / len(tweets),
            "average_subjectivity": subjectivity_sum / len(tweets),
        }

    def analyze_sentiment(self, tweet):
        cleaned_tweet = self.clean_tweet(tweet)
        blob = TextBlob(cleaned_tweet)
        return blob.sentiment

    def load_tweets(self, query, refresh_cache):
        if not refresh_cache:
            try:
                return self.cache.load(f"{cached_data_path}/{query}.txt")
            except FileNotFoundError:
                print("\nCached tweets do not exist. Fetching new tweets.\n")

        tweets = self.load_fresh_tweets(query)
        self.cache.cache(f"{cached_data_path}/{query}.txt", tweets)

        return tweets

    def load_fresh_tweets(self, query):
        try:
            return self.twitter_api.search(query)
        except:
            raise Exception("An error occured while attempting to fetch new tweets.")

    def check_cached_results(self, path):
        results = None
        try:
            results = self.cache.load(path)
        except FileNotFoundError:
            print("\nCached results do not exist.\n")

        return results

    def segment_by_date(self, tweets):
        tweets_by_date = {}

        for tweet in tweets:
            date_time = parse(tweet['created_at'])
            date = str(date_time.date())

            if date in tweets_by_date:
                tweets_by_date[date].append(tweet)
            else:
                tweets_by_date[date] = [tweet]

        return tweets_by_date

    def clean_tweet(self, tweet):
        return " ".join(
            re.sub(
                r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet
            ).split()
        )
