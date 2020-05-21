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

    tweets_state_usr = [json.loads(line)['user'].get('location') for line in fp
                        if 'created_at' in json.loads(line)
                        and not json.loads(line).get('is_quote_status', False)
                        and not json.loads(line).get('text', 'RT').startswith('RT')]
    fp.seek(0)

    tweets_state_place = []
    for line in fp:
        if not json.loads(line).get('is_quote_status', False) and not json.loads(line).get('text', 'RT').startswith('RT'):
            tweet = json.loads(line)
            if tweet['place'] is not None:
                tweets_state_place.append(tweet['place'].get('full_name'))
            else:
                tweets_state_place.append(None)

    for index, (a, b) in enumerate(zip(tweets_state_usr, tweets_state_place)):
        if a is None and b is not None:
            tweets_state_usr[index] = b
        elif a is None and b is None:
            del a[index]
            del b[index]
    return tweets_state_usr


def main():
    json_file = open(sys.argv[1])
    tweets_state = parse_json(json_file)


if __name__ == '__main__':
    main()
