# Business Sentiment Analyzer

## Introduction

A Python library for performing sentiment analysis on tweets of a particular business of interest. It uses TextBlob, a Python library built on top of NLTK, capable of determining the sentiment of various pieces of text.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Requirements

Python >= 3.7

### Installing

Clone the repository with:

```
$ git clone git@github.com:mazenkurdi/business-sentiment-analyzer.git
```

To install dependencies, run:

```
pipenv shell
pipenv install
```

### Running

Import app

```
from bsa import Bsa
```

Set twitter credentials. Missing credentials will prevent you from fetching new tweets. You will only be able to run the app on cached data (See available cached data below for testing).

```
twitter_credentials = {
    "consumer_key": your_consumer_key,
    "consumer_secret": your_consumer_secret,
    "access_token": your_access_token,
    "access_token_secret": your_access_token_secret,
}

bsa = Bsa(twitter_credentials)
```

If twitter credentials are missing, initialize app with no arguments:

```
bsa = Bsa()
```

Run analyze function for a business name and specify options. Detailed documentation below:

```
business_name = "Apple"
opts = { 'refresh_cache': True }

bsa.analyze(business_name, opts)
```

### analyze(business_name, opts):

Analyze the public perception of the business given by business_name.

Takes an additional opts parameter which can include:

```
refresh_cache: When True, new data will be fetched and analyzed
print_results: When True, results will be printed out in the terminal
with_time_context: When True, results will be segmented per day
```

Returns an array of objects:

```
[{
    "date": date or None
    "number_of_tweets": int,
    "number_of_positive_tweets": int,
    "number_of_neutral_tweets": int,
    "number_of_negative_tweets": int,
    "average_polarity": float,
    "average_subjectivity": float
}]
```

## Testing

For testing purposes, see test.py, which should have the app imported and set up

## Cached Data

With no twitter credentials, you can run the app using cached data (refresh_cache must be set to False). See list below for business names with cached data:

- Apple
- Burger King
- Facebook
- Instagram
- Rakuten
- Shopify
- Starbucks
- WeWork
- WealthSimple


## How it works

1. The analyze function is run with a specific business name

2. If refresh_cache is set to True, bsa will first make a search call to Twitter's api with the business name as the query

3. Upon receiving the tweets, they will be cached for future use

4. If with_time_context is set to True, the tweets will be segmented per date, otherwise they will be regarded as one whole batch

5. Each tweet will then be cleaned and run through a sentiment analyzer to receive a polarity and subjectivity score. This sentiment analyzer is a feature of the TextBlob library, which is built on top of NLTK.

6. The scores for all the tweets will be aggregated to calculate the average polarity and subjectivity for all the tweets as well as the percentage of positive, negative, and neutral tweets.

7. The results of this analysis will also be cached for future use

8. If print_results is set to True (True by default), results will be printed in the terminal
