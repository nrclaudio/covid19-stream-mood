"""
returns the name of the happiest state as a string

You can ignore any tweets for which you cannot assign
a location in the United States

Note: Not every tweet will have a text field --- again,
real data is dirty! Be prepared to debug, and feel free
to throw out tweets that your code can't handle to get
something working. For example, you might choose to
ignore all non-English tweets.

Your script should print the two letter state
abbreviation of the state with the highest average
tweet sentiment to stdout.

Note that you may need a lot of tweets in order to get
enough tweets with location data. Let the live stream
run for a while if you wish.

"""


import sys
import json
import re
from collections import defaultdict, Counter


regex = re.compile("[^a-zA-Z0-9.'-]")


def parse_json(fp):
    """
    ------
    input: tweets file handle
    output: list(hashtags)
    ------

    parses tweets to extract hashtag field into a non-unique list
    """

    hashtags = []
    for i, line in enumerate(fp):
        if 'created_at' in json.loads(line) and not json.loads(line).get('is_quote_status', False) and not json.loads(line).get('text', 'RT').startswith('RT'):

            tweet = json.loads(line)

            for hashtag in tweet['entities']['hashtags']:
                hashtags.append(hashtag['text'])
    return hashtags


def top_ten(hashtag_list):
    hashtag_counter = Counter(hashtag_list)
    return sorted(hashtag_counter.items(), key=lambda x: x[1], reverse=True)[:9]


def main():
    json_file = open(sys.argv[1])
    hashtags = parse_json(json_file)
    top10_hashtags = top_ten(hashtags)
    for i in top10_hashtags:
        print(' '.join(str(x) for x in i))


if __name__ == '__main__':
    main()
