import twitter
from datetime import date, timedelta


class TwitterApi:
    def __init__(
        self, consumer_key, consumer_secret, access_token, access_token_secret
    ):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

        self.api = twitter.Api(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token_key=access_token,
            access_token_secret=access_token_secret,
        )

    def search(self, query):
        date_since = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
        results = self.api.GetSearch(
            raw_query=f"q={query}&since={date_since}&count=100&lang=en"
        )

        return [
            {
                'id': result.AsDict()["id_str"],
                'created_at': result.AsDict()["created_at"],
                'text': result.AsDict()["text"]
            }
            for result in results
        ]
