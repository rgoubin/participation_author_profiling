from nltk import pos_tag, word_tokenize
from nltk.tokenize import TweetTokenizer
from nltk.tag import pos_tag_sents
from nltk import FreqDist
from math import log2
from collections import Counter


class POS_taging:
    '''
    Class for taging words
    '''

    def __init__(self):
        self.possible_tags = ['CC','CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS',
         'LS', 'MD', 'NN', 'NNP', 'NNPS', 'NNS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB',
         'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP',
         'VBZ', 'WDT', 'WP', 'WP$', 'WRB',
         '.', ',', ':', '$', '\'\'', '(', ')', '#', '``']

        ''' text (list(list(str) => should look like str[]
        word_tokenize() might be needed => no need because tweet tokenizer
        '''
    def get_tag_from_text(self, text):
        tokenizr = TweetTokenizer(preserve_case=True,strip_handles=True,reduce_len=False) # should be useful
        new_text = tokenizr.tokenize(text)
        #self.tagged_text = pos_tag_sents(new_text, tagset=None, lang='eng')
        tagged_text = pos_tag(new_text, tagset=None, lang='eng')
        return tagged_text

            # return [' '.join(grams) for grams in n_grams ]
    def get_tag_frequency(self, tagged_text):
        global_counts = {} # initialize dict
        for tag in self.possible_tags:
            global_counts[tag] = 0

        sum_tagged_words = 0;
        counts = Counter(tag for word, tag in tagged_text) # get tag in a sentence
        for tag in counts:
            test = global_counts.get(tag,'error')
            if test == 'error':
                print('tag :' + tag + 'not in dict')
            global_counts[tag] = global_counts.get(tag,0) + counts.get(tag,0)
            sum_tagged_words = sum_tagged_words + counts.get(tag,0)
        for tag in global_counts:
            if sum_tagged_words == 0:
                global_counts[tag] = 0
            else :
                global_counts[tag] = global_counts.get(tag,0)/sum_tagged_words

        # global_counts change to features
        features = []
        for tag in global_counts:
            features.append(global_counts.get(tag,0))
        return features

    '''def get_tag_proportion(self):
        return 0'''

    def pos_tag_all_features(self, author):
        features = []
        tagged_text = []

        for tweet in author['tweets']:
            tagged_text.extend(self.get_tag_from_text(tweet))
        features.extend(self.get_tag_frequency(tagged_text))
        return features

    def analyzer(self, text):
        res = list()
        res += get_tag_from_text(text)
        return res

    def printArgs(self):
        print()

class Word_features:
    '''
    '''
    def __init__(self):
        '''
        useless for now
        '''

    def word_count(self, text):
        word_counter = 0
        for word in text:
            word_counter += 1
        return word_counter

    def shannon(self, dict, total):
        return sum(freq / total * log2(total / freq) for freq in dict.values())

    def word_entropy(self, text, word_count):
        fd = FreqDist(text) # todo import method => done
        return self.shannon(fd, word_count)

    def word_all_features(self, author):
        features = []
        tokenizr = TweetTokenizer(preserve_case=True,strip_handles=True,reduce_len=False) # should be useful
        i = 0
        # mean of word_count and tweet entropy
        total_word_count = 0
        total_entropy = 0
        for tweet in author['tweets']:
            new_text = tokenizr.tokenize(tweet)
            i += 1
            word_count = self.word_count(new_text)
            total_word_count += word_count
            total_entropy += self.word_entropy(new_text, word_count)
        total_word_count = total_word_count/i
        total_entropy = total_entropy/i

        features.append(total_word_count) #need to be done first
        features.append(total_entropy)
        return features
