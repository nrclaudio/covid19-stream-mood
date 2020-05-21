# [# of occurrences of the term in all tweets]/
# [# of occurrences of all terms in all tweets]

import sys
import json
import re
import string
from collections import Counter

regex = re.compile("[^a-zA-Z0-9.'-]")


def strip_punct(word):
    return word.translate(str.maketrans('', '', string.punctuation))


def lines(fp):
    nr = len(fp.readlines())
    fp.seek(0)
    return nr


def parse_json(fp):
    tweets_text = [json.loads(line)['text'] for line in fp
                   if 'created_at' in json.loads(line)
                   and not json.loads(line).get('is_quoted_status', False)
                   and not json.loads(line).get('text', 'RT').startswith('RT')]
    return tweets_text


def term_frequency(texts):
    word = Counter()
    word_freq = {}
    for text in texts:
        words = [regex.sub('', strip_punct(word).lower())
                 for word in text.split(' ') if not word.startswith(("https"))]
        word.update(Counter(words))
    word_freq.update({k: (v / sum(word.values()))for (k, v) in word.items()})
    return word_freq


def main():
    json_file = open(sys.argv[1])
    tweets_text = parse_json(json_file)
    frequencies = term_frequency(tweets_text)
    for key in frequencies:
        print("{} {}".format(key, frequencies[key]))


if __name__ == '__main__':
    main()
