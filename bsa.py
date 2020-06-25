from src import BusinessSentimentAnalyzer

default_tokens = {
    'consumer_key': '',
    'consumer_secret': '',
    'access_token': '',
    'access_token_secret': ''
}

class Bsa:
    def __init__(self, twitter_credentials=default_tokens):
        self.app = BusinessSentimentAnalyzer(twitter_credentials)

    def analyze(self, business_name, opts={}):
        """
        Analyze the public perception of the business given
        by business_name.

        Takes an additional opts parameter which can include:
            refresh_cache: When True, new data will be fetched and analyzed
            print_results: When True, results will be printed out in the terminal
            with_time_context: When True, results will be segmented per day

        Returns an array of objects:
            [{
                "date": date or None
                "number_of_tweets": int,
                "number_of_positive_tweets": int,
                "number_of_neutral_tweets": int,
                "number_of_negative_tweets": int,
                "average_polarity": float,
                "average_subjectivity": float
            }]
        """

        # Default opt values
        params = {
            "refresh_cache": False,
            "print_results": True,
            "with_time_context": False
        }

        if "refresh_cache" in opts:
            params["refresh_cache"] = opts["refresh_cache"]

        if "print_results" in opts:
            params["print_results"] = opts["print_results"]

        if "with_time_context" in opts:
            params["with_time_context"] = opts["with_time_context"]

        return self.app.analyze(business_name, params)
