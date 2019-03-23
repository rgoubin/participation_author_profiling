# coding=utf-8
import re
import string
from nltk.corpus import stopwords
from giovanniScripts.sstemmer_copy import SStemmer
from nltk.tokenize import TweetTokenizer
import emojis


class clean_en_txt:

    first_person = ['i', 'me', 'my', 'myself',
                    'we', 'our', 'ours', 'ourselves', ]

    pronouns = ['you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
                'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', ]

    negation = ['don', "don't", 'should', 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'mightn', "mightn't", 'mustn',
                "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't",
                'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't",
                'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

    stopwordsssss = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're",
                     "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he',
                     'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's",
                     'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
                     'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was',
                     'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
                     'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
                     'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during',
                     'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
                     'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
                     'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
                     'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just',
                     'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain',
                     'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't",
                     'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn',
                     "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't",
                     'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

    punctuations_list = string.punctuation
    stopwords_list = stopwords.words('english')

    def __init__(self):
        pass

    def normalize(self, text):
        return text

    def remove_punctuations(self, text):
        translator = str.maketrans('', '', clean_en_txt.punctuations_list)
        return text.translate(translator)

    def remove_repeating_char(self, text):
        return re.sub(r'(.)\1+', r'\1', text)

    def label_stopwords(self, text):
        '''for word in clean_en_txt.first_person:
            text = text.replace(' ' + word + ' ', ' <first_person> ')
        for word in clean_en_txt.pronouns:
            text = text.replace(' ' + word + ' ', ' <pronoun> ')
        # print(text)
        return text'''
        for word in clean_en_txt.first_person:
            text = text.replace(' ' + word + ' ', ' <first_person> ')
            text = text.replace(' ' + word + '\'', ' <first_person> ')
        for word in clean_en_txt.pronouns:
            text = text.replace(' ' + word + ' ', ' <pronoun> ')
        for word in clean_en_txt.negation:
            text = text.replace(' ' + word + ' ', ' <negation> ')
        # print(text)
        return text

    def delete_hashtag(self, text):
        # https://gist.github.com/mahmoud/237eb20108b5805aed5f
        hashtag_re = re.compile("(?:^|\s)[＃#]{1}(\w+)", re.UNICODE)
        list_hashtags = hashtag_re.findall(text)
        for hashtag in list_hashtags:
            text = text.replace(hashtag, '')
        # print(text)
        return text

    def label_user_mentions(self, text):
        # https://gist.github.com/mahmoud/237eb20108b5805aed5f
        mention_re = re.compile(
            "(?:^|\s)[＠ @]{1}([^\s#<>[\]|{}]+)", re.UNICODE)
        list_mentions = mention_re.findall(text)
        for mention in list_mentions:
            text = text.replace(mention, '<user_mention>')
        # print(text)
        return text

    def label_URLs(self, text):
        return re.sub(u'https?:\/\/[^\s-]*', ' ', text, flags=re.MULTILINE)

    def tokenize(self, text):
        stemmer = SStemmer()
        text = self.remove_punctuations(text)
        text = self.delete_hashtag(text)

        '''list_emo = emojis.get(text)
        for emoji in list_emo:
            text = text.replace(emoji, '')'''

        #text = self.label_URLs(text)
        #text = self.label_user_mentions(text)
        text = self.remove_repeating_char(text)
        text = self.label_stopwords(text)

        tokenizer = TweetTokenizer()
        tokens = tokenizer.tokenize(text)
        stemmed_tokens = []
        for token in tokens:
            '''if token not in clean_en_txt.stopwords_list:
                stemmed_tokens.append(stemmer.stem(token))'''
            if token.lower() not in clean_en_txt.stopwords_list:
                stemmed_tokens.append(stemmer.stem(token.lower()))
        return tokens
        # return [stemmer.stem(x) for x in text.split() if stemmer.stem(x) not in clean_en_txt.stopwords_list]
