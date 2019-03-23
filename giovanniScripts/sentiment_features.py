import re

class Sentiment_extractor:
# Class for extrating sentiment related features
    def __init__(self):
        self.ratio = 0
        #todo
    def emoticon_ratio(self, author):
        tweet_having_emoticon = 0
        emoticon_number = 0
        for tweet in author['tweets']:
            emoticon_number = len(re.findall(u'[\U0001f600-\U0001f650]', tweet))
            if emoticon_number > 0:
                tweet_having_emoticon += 1
        return tweet_having_emoticon/len(author['tweets'])
