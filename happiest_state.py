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


states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}


def parse_json(fp):
    """
    ------
    input: tweets file handle
    output: list(tweets)
    ------

    parses tweets to extract text field usr location data and place location data if available. It also returns the text in the tweet for sentiment inference
    """

    tweets = defaultdict(lambda: defaultdict(int))
    for i, line in enumerate(fp):
        if 'created_at' in json.loads(line) and not json.loads(line).get('is_quote_status', False) and not json.loads(line).get('text', 'RT').startswith('RT'):

            tweet = json.loads(line)

            tweets[i]['text'] = tweet['text']
            if tweet['user']['location'] is not None:
                tweets[i]['state_usr'] = tweet['user'].get('location')
            elif tweet['user']['location'] is None:
                tweets[i]['state_usr'] = 'state_usr not defined'
            if tweet['place'] is not None:
                tweets[i]['state_place'] = tweet['place'].get('full_name')
            elif tweet['place'] is None:
                tweets[i]['state_place'] = 'state_place not defined'
    return tweets


def sent_dict(fp):
    dict_afinn = {word: value.rstrip('\n') for line in fp
                  for word, value in (line.split('\t'),)}
    fp.seek(0)
    return dict_afinn


def tweet_sent(tweets_dict, scores):
    """
    creates a new key for the tweet with its sentiment score
    """
    for tweet in tweets_dict:
        words = [regex.sub('', word) for word in tweets_dict[tweet]['text'].split(
            ' ') if not word.startswith(("https"))]
        tweets_dict[tweet]['score'] = sum(
            int(scores.get(word, 0)) for word in words)
    return tweets_dict


def tweet_state(tweets_score):
    """
    creates a new key for the intersection between user defined
    location and twitter determined location
    """
    for tweet in tweets_score:
        if tweets_score[tweet]['state_place'] is not None and ',' in tweets_score[tweet]['state_place']:
            tweets_score[tweet]['state'] = tweets_score[tweet]['state_place'].split(', ')[
                1]
        else:
            tweets_score[tweet]['state'] = tweets_score[tweet]['state_usr']
    return tweets_score


def state_score(tweets_state):
    """
    returns a dictionary with the score per state
    """
    state_score = defaultdict(int)
    state_count = Counter()
    for key, val in tweets_state.items():
        if val['state'] in states:
            state_count.update([val['state']])
            state_score[val['state']] += val['score']

    state_score = {k: v / state_count[k] for (k, v) in state_score.items()}

    return state_score


def main():
    sent_file = open(sys.argv[1])
    json_file = open(sys.argv[2])
    tweets_text = parse_json(json_file)
    scores = sent_dict(sent_file)
    tweets_score = tweet_sent(tweets_text, scores)
    tweets_state = tweet_state(tweets_score)
    state_scores = state_score(tweets_state)
    print(max(state_scores, key=lambda key: state_scores[key]))


if __name__ == '__main__':
    main()
