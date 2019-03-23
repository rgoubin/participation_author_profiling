# coding=utf-8
import re
import string
from nltk.corpus import stopwords
from giovanniScripts.sstemmer_copy import SStemmer
#import sstemmer_copy

first_person = ['I', 'i', 'me', 'my', 'myself',
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


def normalize(text):
    return text


def remove_punctuations(text, do_label=True):
    # print(punctuations_list)
    punctuations_list_filtered = punctuations_list
    if do_label:
        punctuations_list_filtered = punctuations_list.replace('#', '')
        punctuations_list_filtered = punctuations_list_filtered.replace(
            '@', '')
        punctuations_list_filtered = punctuations_list_filtered.replace(
            '\'', '')

    # print(punctuations_list_filtered)
    translator = str.maketrans('', '', punctuations_list_filtered)
    return text.translate(translator)


def remove_repeating_char(text):
    return re.sub(r'(.)\1+', r'\1', text)


def label_stopwords(text):
    for word in first_person:
        text = text.replace(' ' + word + ' ', ' <first_person> ')
        text = text.replace(' ' + word + '\'', ' <first_person> ')
    for word in pronouns:
        text = text.replace(' ' + word + ' ', ' <pronoun> ')
    for word in negation:
        text = text.replace(' ' + word + ' ', ' <negation> ')
    # print(text)
    return text


def label_hashtag(text):
    # https://gist.github.com/mahmoud/237eb20108b5805aed5f
    hashtag_re = re.compile("(?:^|\s)[##]{1}(\w+)", re.UNICODE)
    list_hashtags = set(hashtag_re.findall(text))
    # print(list_hashtags)
    for hashtag in list_hashtags:
        text = text.replace('#' + hashtag, ' <hashtag> ')
    # print(text)
    return text


def label_user_mentions(text):
    # https://gist.github.com/mahmoud/237eb20108b5805aed5f
    mention_re = re.compile(
        "(?:^|\s)[@@]{1}([^\s#<>[\]|{}]+)", re.UNICODE)
    list_mentions = set(mention_re.findall(text))
    #print('list mention')
    # print(list_mentions)
    for mention in list_mentions:
        text = text.replace('@' + mention, ' <user_mention> ')

    return text


def stemmer(text):
    stemmer = SStemmer()
    stemmed_tokens = [stemmer.stem(x) for x in text.split(
    ) if stemmer.stem(x) not in stopwords_list]
    return ' '.join(stemmed_tokens)


def tokenize(text, do_label=True):

    # print(text)

    #text = self.normalize(text)
    text = remove_punctuations(text, do_label)
    if do_label:
        text = label_user_mentions(text)
        text = label_hashtag(text)
        text = label_stopwords(text)
    else:
        #stemmer = SStemmer()
        # return [stemmer.stem(x) for x in text.split() if stemmer.stem(x) not in stopwords_list]
        text = stemmer(text)
    text = remove_repeating_char(text)
    # print(text)
    #text = None
    # text.count('<hashtag>')
    return text
    # return  text.split()
