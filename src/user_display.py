divider = "===============================================================\n\n"


class UserDisplay:
    def display(self, query, results):
        for result in results:
            self.display_result(query, result)

    def display_result(self, query, results):
        number_of_tweets = results['number_of_tweets']

        displayed_results = ""
        displayed_results += divider
        displayed_results += f"Results for {query}\n\n"

        if results['date']:
            displayed_results += f"Date: {results['date']}\n\n"

        displayed_results += (
            f"Number of tweets analyzed: {number_of_tweets}\n"
        )
        displayed_results += (
            f"Percentage of positive tweets: {100 * results['number_of_positive_tweets'] / number_of_tweets}%\n"
        )
        displayed_results += (
            f"Percentage of neutral tweets: {100 * results['number_of_neutral_tweets'] / number_of_tweets}%\n"
        )
        displayed_results += (
            f"Percentage of negative tweets: {100 * results['number_of_negative_tweets'] / number_of_tweets}%\n\n"
        )
        displayed_results += (
            f"General view: {self.describe_polarity(results['average_polarity'])}\n"
        )
        displayed_results += f"Total Polarity: {results['average_polarity']}\n"
        displayed_results += (
            f"Total Subjectivity: {results['average_subjectivity']}\n\n"
        )

        displayed_results += divider
        print(displayed_results)

    def describe_polarity(self, polarity):
        if polarity > 0:
            description = "The public perception is positive."
        elif polarity == 0:
            description = "The public perception is neutral."
        else:
            description = "The public perception is negative."

        return description
