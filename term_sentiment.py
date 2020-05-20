import sys
import json
import re
import string
import itertools
import math
import operator
from collections import Counter

regex = re.compile("[^a-zA-Z0-9.'-]")


def lines(fp):
    nr = len(fp.readlines())
    fp.seek(0)
    return nr


def strip_punct(word):
    return word.translate(str.maketrans('', '', string.punctuation))


def sent_dict(fp):
    dict_afinn = {word: value.rstrip('\n') for line in fp
                  for word, value in (line.split('\t'),)}
    return dict_afinn


def parse_json(fp):
    tweets_text = [json.loads(line)['text'] for line in fp
                   if not json.loads(line)['is_quote_status']
                   and not json.loads(line)['text'].startswith('RT')]
    return tweets_text


def norm(sentiments, counts):
    ret = dict()
    for key, sentiment in sentiments.items():
        ret[key] = sentiment + math.log10(counts.get(key, 1))
    return ret


def inner_infer_sent(texts, scores):
    inner_sent = {}
    word_count = Counter()
    for text in texts:
        words = [regex.sub('', strip_punct(word).lower())
                 for word in text.split(' ') if not word.startswith(("https"))]
        word_count.update(Counter(words))
        if any(word in scores for word in words):
            for i, word in enumerate(words):
                if len(word) < 4:
                    inner_sent[word] = 0
                else:
                    inner_sent[word] = inner_sent.get(word, 0)
                    prior_words = words[0: i]
                    posterior_words = words[i + 1: len(words)]
                    for index, (prior, posterior) in enumerate(itertools.zip_longest(posterior_words, prior_words)):
                        inner_sent[word] += sum([int(scores.get(prior, 0)),
                                                 int(scores.get(posterior, 0))]) / (index + 1)
    inner_sent = norm(inner_sent, word_count)
    return inner_sent


def tweet_sent(texts, scores):
    sentiments = []
    for text in texts:
        words = [regex.sub('', strip_punct(word).lower())
                 for word in text.split(' ') if not word.startswith(("https"))]
        sentiments.append(sum(int(scores.get(word, 0)) for word in words))
    return sentiments


def infer_sent_term(texts, scores):
    inner_sent = inner_infer_sent(texts, scores)
    sentiments = tweet_sent(texts, scores)

    sent = {}
    for i, text in enumerate(texts):
        words = [regex.sub('', strip_punct(word).lower())
                 for word in text.split(' ') if not word.startswith(("https"))]
        if sentiments[i] != 0:
            for word in words:
                if word in scores:
                    break
                else:
                    sent[word] = sent.get(word, (0, 0))
                    if sentiments[i] > 0:
                        sent[word] = tuple(
                            map(operator.add, (1, 0), sent[word]))
                    elif sentiments[i] < 0:
                        sent[word] = tuple(
                            map(operator.add, (0, -1), sent[word]))
    sent.update((k, sum(list(v)) + inner_sent.get(k, 0))
                for k, v in sent.items())
    return sent


def main():
    sent_file = open(sys.argv[1])
    json_file = open(sys.argv[2])
    sent_scores = sent_dict(sent_file)
    tweets_text = parse_json(json_file)
    sent = infer_sent_term(tweets_text, sent_scores)
    for key in sent:
        print("{} {}".format(key, sent[key]))


if __name__ == '__main__':
    main()
