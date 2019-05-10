import re
from nltk.tokenize import TweetTokenizer
from nltk.stem import SnowballStemmer

class Sentiment_analysis: #spanish only
    def __init__(self):
        self.dal_path = "./SpanishDAL-v1.2/meanAndStdev.csv"
        self.stemmer = SnowballStemmer('spanish')
        self.tokenizr = TweetTokenizer(preserve_case=True,strip_handles=True,reduce_len=False) # should be useful
        self.read_dal()

    def read_dal(self):
        self.dal_dict = {}
        # dal_list = [] useless
        with open(self.dal_path) as file:
            for line in file:
                dal = []
                #creating structure
                line = line.rstrip('\n')
                dal = line.split(";")
                word = dal.pop(0)
                #clean word
                word = word.strip('_')[0]
                #stemming
                word = self.stemmer.stem(word)
                # test if stemming is needed
                # dal_list.append(dal) useless
                #cast string to int
                dal = [float(i) for i in dal]
                #add to dictionary
                self.dal_dict[word] = dal;

    def analyse_author(self, author):
        overall_values = [0] * 6 # 6 values
        author_tweets_number = len(author['tweets'])
        '''
        pleasantness_mean
        activation_mean
        imagery_mean
        pleasantness_stdev
        activation_stdev
        imagery_stdev
        '''
        for tweet in author['tweets']:
            values = self.analyse_tweet(tweet)
            i = 0
            for overall_value in overall_values:
                overall_value = overall_value + values[i]
                i = i + 1
        for overall_value in overall_values:
            overall_value = overall_value / author_tweets_number
        return overall_values

    def analyse_tweet(self, tweet):
        curent_values = [0] * 6
        text = self.tokenizr.tokenize(tweet)
        word_found = 0
        for word in tweet:
            word = self.stemmer.stem(word)
            result = self.find_word(word)
            if result[0]:
                word_values = result[1]
                i = 0
                for value in word_values:
                    curent_values[i] = curent_values[i] + value
                    i = i + 1
                word_found = word_found + 1
        if word_found != 0:
            for value in curent_values:
                value = value / word_found
        return curent_values
    def find_word(self, word):
        result = self.dal_dict.get(word, None)
        if result == None:
            return (False, [])
        else:
            return (True, result)
