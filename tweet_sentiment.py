import sys
import json
import re

regex = re.compile("[^a-zA-Z0-9.'-]")


def sent_dict(fp):
    dict_afinn = {word: value.rstrip('\n') for line in fp
                  for word, value in (line.split('\t'),)}
    return dict_afinn


def parse_json(fp):
    tweets_text = [json.loads(line)['text'] for line in fp
                   if not json.loads(line)['is_quote_status']
                   and not json.loads(line)['retweeted']
                   and not json.loads(line)['text'].startswith('RT')]
    return tweets_text


def tweet_sent(texts, scores):
    sentiments = []
    for text in texts:
        words = [regex.sub('', word) for word in text.split(' ') if not word.startswith(("https"))]
        sentiments.append(sum(int(scores.get(word, 0)) for word in words))
    return sentiments


def main():
    sent_file = open(sys.argv[1])
    json_file = open(sys.argv[2])
    sent_scores = sent_dict(sent_file)
    tweets_text = parse_json(json_file)
    sentiments = tweet_sent(tweets_text, sent_scores)
    print("\n".join(map(str, sentiments)))


if __name__ == '__main__':
    main()
