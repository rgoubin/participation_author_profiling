import re
import statistics as stats
from nltk.tokenize import TweetTokenizer
from nltk import FreqDist
from math import log2
import emojis
# Add the features directly into the dictionary


def number_of_words_1(Authors):
    for author in Authors:
        number_of_words = 0
        for tweet in author['tweets']:
            number_of_words = number_of_words + len(tweet.split())
        author['number_of_words'] = number_of_words/100


# Return a list of the features of all the users
def number_of_words_2(Authors):
    features = []
    for author in Authors:
        number_of_words = 0
        for tweet in author['tweets']:
            number_of_words = number_of_words + len(tweet.split())
        features.append(number_of_words/100)

    return features


def standart_deviation_1(Authors):
    for author in Authors:
        list_length = []
        for tweet in author['tweets']:
            list_length.append(len(tweet))
        author['standart_deviation'] = stats.stdev(list_length)


# Return a list of the features of all the users
def standart_deviation_2(Authors):

    features = []
    for author in Authors:
        list_length = []
        for tweet in author['tweets']:
            list_length.append(len(tweet))
        features.append(stats.stdev(list_length))
    return features


def tweet_length_1(Authors):
    for author in Authors:
        tweet_length = 0
        for tweet in author['tweets']:
            tweet_length = tweet_length + len(tweet)
        author['tweet_length'] = tweet_length/100


def tweet_length_2(Authors):
    features = []

    for author in Authors:
        tweet_length = 0
        for tweet in author['tweets']:
            tweet_length = tweet_length + len(tweet)
        features.append(tweet_length/100)

    return features


def URL_1(Authors):
    url_re = re.compile(u'https?:\/\/[^\s-]*', re.UNICODE)
    for author in Authors:
        urls = 0
        for tweet in author['tweets']:
            list_url = url_re.findall(tweet)
            urls = urls + len(list_url)
        author['url'] = urls


# Return a list of the features of all the users
def URL_2(Authors):
    url_re = re.compile(u'https?:\/\/[^\s-]*', re.UNICODE)

    features = []
    for author in Authors:
        urls = 0
        for tweet in author['tweets']:
            list_url = url_re.findall(tweet)
            urls = urls + len(list_url)
        features.append(urls)

    return features


def hashtags_1(Authors):
    # https://gist.github.com/mahmoud/237eb20108b5805aed5f
    hashtag_re = re.compile("(?:^|\s)[##]{1}(\w+)", re.UNICODE)
    for author in Authors:
        hashtags = 0
        for tweet in author['tweets']:
            list_hashtags = hashtag_re.findall(tweet)
            hashtags = hashtags + len(list_hashtags)
        author['hashtags'] = hashtags


# Return a list of the features of all the users
def hashtags_2(Authors):
    # https://gist.github.com/mahmoud/237eb20108b5805aed5f
    hashtag_re = re.compile("(?:^|\s)[##]{1}(\w+)", re.UNICODE)

    features = []
    for author in Authors:
        hashtags = 0
        for tweet in author['tweets']:
            list_hashtags = hashtag_re.findall(tweet)
            hashtags = hashtags + len(list_hashtags)
        features.append(hashtags)

    return features

# Return a list of the features of all the users
def hashtags_3(author):
    # https://gist.github.com/mahmoud/237eb20108b5805aed5f
    hashtag_re = re.compile("(?:^|\s)[##]{1}(\w+)", re.UNICODE)

    features = []
    hashtags = 0
    for tweet in author['tweets']:
        list_hashtags = hashtag_re.findall(tweet)
        hashtags = hashtags + len(list_hashtags)
    features.append(hashtags)

    return features

def user_mentions_1(Authors):
    # https://gist.github.com/mahmoud/237eb20108b5805aed5f
    mention_re = re.compile(
        "(?:^|\s)[@@]{1}([^\s#<>[\]|{}]+)", re.UNICODE)

    for author in Authors:
        user_mentions = 0
        for tweet in author['tweets']:
            list_mentions = mention_re.findall(tweet)
            user_mentions = user_mentions + len(list_mentions)
        author['user_mentions'] = user_mentions


# Return a list of the features of all the users
def user_mentions_2(Authors):
    # https://gist.github.com/mahmoud/237eb20108b5805aed5f
    mention_re = re.compile(
        "(?:^|\s)[@@]{1}([^\s#<>[\]|{}]+)", re.UNICODE)

    features = []
    for author in Authors:
        user_mentions = 0
        for tweet in author['tweets']:
            list_mentions = mention_re.findall(tweet)
            user_mentions = user_mentions + len(list_mentions)
        features.append(user_mentions)

    return features

def user_mentions_3(author):
    # https://gist.github.com/mahmoud/237eb20108b5805aed5f
    mention_re = re.compile(
        "(?:^|\s)[@@]{1}([^\s#<>[\]|{}]+)", re.UNICODE)

    features = []
    user_mentions = 0
    for tweet in author['tweets']:
        list_mentions = mention_re.findall(tweet)
        user_mentions = user_mentions + len(list_mentions)
    features.append(user_mentions)

    return features

def emoticon_ratio(author):
    tweet_having_emoticon = 0
    emoticon_number = 0
    for tweet in author['tweets']:
        # emoticon_number = len(re.findall(u'[\U0001f600-\U0001f650]', tweet))
        emoticon_number = emojis.count(tweet)
        if emoticon_number > 0:
            tweet_having_emoticon += 1
    return tweet_having_emoticon/len(author['tweets'])

def emoticon_number_avg(author):
    emoticon_number = 0
    for tweet in author['tweets']:
        # emoticon_number = len(re.findall(u'[\U0001f600-\U0001f650]', tweet))
        emoticon_number += emojis.count(tweet)
    return emoticon_number/len(author['tweets'])

def emoticon_number_sd(author):
    emoticon_number_list = []
    for tweet in author['tweets']:
        # emoticon_number = len(re.findall(u'[\U0001f600-\U0001f650]', tweet))
        emoticon_number_list.append(emojis.count(tweet))
    sd = stats.stdev(emoticon_number_list)
    return sd

def all_emoticon_features(author):
    all_features = []
    all_features.append(emoticon_ratio(author))
    all_features.append(emoticon_number_avg(author))
    all_features.append(emoticon_number_sd(author))
    return all_features

def word_count(text):
    word_counter = 0
    for word in text:
        word_counter += 1
    return word_counter


def shannon_entropy(dict, total):
    return sum(freq / total * log2(total / freq) for freq in dict.values())


def word_entropy(text, word_count):
    fd = FreqDist(text)  # todo import method => done
    return shannon_entropy(fd, word_count)


def word_all_features(author):
    features = []
    tokenizr = TweetTokenizer(
        preserve_case=True, strip_handles=True, reduce_len=False)  # useful
    i = 0
    # mean of word_count and tweet entropy
    total_word_count = 0
    total_entropy = 0
    for tweet in author['tweets']:
        new_text = tokenizr.tokenize(tweet)
        i += 1
        word_count_tweet = word_count(new_text)
        total_word_count += word_count_tweet
        total_entropy += word_entropy(new_text, word_count_tweet)
    total_word_count = total_word_count/i
    total_entropy = total_entropy/i

    features.append(total_word_count)  # need to be done first
    features.append(total_entropy)
    return features


def pourcent_upper_1(Authors):
    upper_re = re.compile(r'[A-Z]')
    lower_re = re.compile(r'[a-z]')

    features = []
    for author in Authors:
        uppercases = 0
        lowercases = 0
        for tweet in author['tweets']:
            uppercases = uppercases + len(upper_re.findall(tweet))
            lowercases = lowercases + len(lower_re.findall(tweet))
        author['uppercase'] = uppercases/(uppercases + lowercases)


# Return a list of the features of all the users
def pourcent_upper_2(Authors):
    upper_re = re.compile(r'[A-Z]')
    lower_re = re.compile(r'[a-z]')

    features = []
    for author in Authors:
        uppercases = 0
        lowercases = 0
        for tweet in author['tweets']:
            uppercases = uppercases + len(upper_re.findall(tweet))
            lowercases = lowercases + len(lower_re.findall(tweet))
        features.append(uppercases/(uppercases + lowercases))

    return features


def all_generic_features(Authors):
    url_re = re.compile(u'https?:\/\/[^\s-]*', re.UNICODE)

    # https://gist.github.com/mahmoud/237eb20108b5805aed5f
    hashtag_re = re.compile("(?:^|\s)[##]{1}(\w+)", re.UNICODE)

    # https://gist.github.com/mahmoud/237eb20108b5805aed5f
    mention_re = re.compile(
        "(?:^|\s)[@@]{1}([^\s#<>[\]|{}]+)", re.UNICODE)

    upper_re = re.compile(r'[A-Z]')
    lower_re = re.compile(r'[a-z]')

    features = []

    for author in Authors:
        features_user = []
        number_of_words = 0
        tweet_length = 0
        urls = 0
        hashtags = 0
        user_mentions = 0
        uppercases = 0
        lowercases = 0
        list_length = []
        #emoticon_ratio_feature = emoticon_ratio(author)
        aggregated_word_count_and_entropy = word_all_features(author)  # list

        for tweet in author['tweets']:
            number_of_words = number_of_words + len(tweet.split())
            tweet_length = tweet_length + len(tweet)
            list_length.append(len(tweet))

            list_url = url_re.findall(tweet)
            urls = urls + len(list_url)

            list_hashtags = hashtag_re.findall(tweet)
            hashtags = hashtags + len(list_hashtags)

            list_mentions = mention_re.findall(tweet)
            user_mentions = user_mentions + len(list_mentions)

            uppercases = uppercases + len(upper_re.findall(tweet))
            lowercases = lowercases + len(lower_re.findall(tweet))

        # print(len(author['tweets']))
        features_user.append(number_of_words/100)
        features_user.append(tweet_length/100)
        features_user.append(stats.stdev(list_length))
        # features_user.append(emoticon_ratio_feature)
        features_user.append(urls)
        features_user.append(hashtags)
        features_user.append(user_mentions)
        '''if (uppercases + lowercases) == 0:
            features_user.append(0)
        else:
            features_user.append(uppercases/(uppercases + lowercases))'''
        # don't use append
        features_user.extend(aggregated_word_count_and_entropy)
        features.append(features_user)

    return features


def all_generic_features_label(Authors):
    url_re = re.compile(u'https?:\/\/[^\s-]*', re.UNICODE)

    # https://gist.github.com/mahmoud/237eb20108b5805aed5f
    hashtag_re = re.compile("(?:^|\s)[##]{1}(\w+)", re.UNICODE)

    # https://gist.github.com/mahmoud/237eb20108b5805aed5f
    mention_re = re.compile(
        "(?:^|\s)[@@]{1}([^\s#<>[\]|{}]+)", re.UNICODE)

    upper_re = re.compile(r'[A-Z]')
    lower_re = re.compile(r'[a-z]')

    features = []

    for author in Authors:
        features_user = []
        number_of_words = 0
        tweet_length = 0
        urls = 0
        hashtags = 0
        user_mentions = 0
        uppercases = 0
        lowercases = 0
        list_length = []
        emoticon_ratio_feature = emoticon_ratio(author)
        aggregated_word_count_and_entropy = word_all_features(author)  # list

        for tweet in author['tweets']:
            number_of_words = number_of_words + len(tweet.split())
            tweet_length = tweet_length + len(tweet)
            list_length.append(len(tweet))

            list_url = url_re.findall(tweet)
            urls = urls + len(list_url)

            list_hashtags = hashtag_re.findall(tweet)
            hashtags = hashtags + len(list_hashtags)

            list_mentions = mention_re.findall(tweet)
            user_mentions = user_mentions + len(list_mentions)

            uppercases = uppercases + len(upper_re.findall(tweet))
            lowercases = lowercases + len(lower_re.findall(tweet))

        # print(len(author['tweets']))
        features_user.append(number_of_words/100)
        # features_user.append(tweet_length/100)
        features_user.append(stats.stdev(list_length))
        # features_user.append(emoticon_ratio_feature)
        features_user.append(urls)
        # features_user.append(hashtags)
        features_user.append(user_mentions)
        if (uppercases + lowercases) == 0:
            features_user.append(0)
        else:
            features_user.append(uppercases/(uppercases + lowercases))
        # don't use append
        # features_user.extend(aggregated_word_count_and_entropy)
        features_user.append(aggregated_word_count_and_entropy[0])
        features.append(features_user)

    return features


def all_generic_features_csv(Authors):
    url_re = re.compile(u'https?:\/\/[^\s-]*', re.UNICODE)

    # https://gist.github.com/mahmoud/237eb20108b5805aed5f
    hashtag_re = re.compile("(?:^|\s)[##]{1}(\w+)", re.UNICODE)

    # https://gist.github.com/mahmoud/237eb20108b5805aed5f
    mention_re = re.compile(
        "(?:^|\s)[@@]{1}([^\s#<>[\]|{}]+)", re.UNICODE)

    upper_re = re.compile(r'[A-Z]')
    lower_re = re.compile(r'[a-z]')

    features = []

    for author in Authors:
        features_user = []
        number_of_words = 0
        tweet_length = 0
        urls = 0
        hashtags = 0
        user_mentions = 0
        uppercases = 0
        lowercases = 0
        list_length = []
        emoticon_ratio_feature = emoticon_ratio(author)
        aggregated_word_count_and_entropy = word_all_features(author)  # list

        for tweet in author['tweets']:
            number_of_words = number_of_words + len(tweet.split())
            tweet_length = tweet_length + len(tweet)
            list_length.append(len(tweet))

            list_url = url_re.findall(tweet)
            urls = urls + len(list_url)

            list_hashtags = hashtag_re.findall(tweet)
            hashtags = hashtags + len(list_hashtags)

            list_mentions = mention_re.findall(tweet)
            user_mentions = user_mentions + len(list_mentions)

            uppercases = uppercases + len(upper_re.findall(tweet))
            lowercases = lowercases + len(lower_re.findall(tweet))

        # print(len(author['tweets']))
        features_user.append(number_of_words/100)
        features_user.append(tweet_length/100)
        features_user.append(stats.stdev(list_length))
        features_user.append(emoticon_ratio_feature)
        features_user.append(urls)
        features_user.append(hashtags)
        features_user.append(user_mentions)
        if (uppercases + lowercases) == 0:
            features_user.append(0)
        else:
            features_user.append(uppercases/(uppercases + lowercases))
        # don't use append
        features_user.extend(aggregated_word_count_and_entropy)
        features.append(features_user)

    return features


def all_generic_bot_features(Authors, lang):
    import giovanniScripts.pos_tag_features as pos_tag_features
    import giovanniScripts.sentiment_features as sentiment_features
    i=0
    features = []
    pos_tag = pos_tag_features.POS_taging()
    if lang == 'es':
        sentiment_analysis = sentiment_features.Sentiment_analysis()

    for author in Authors:

        features_user = []

        emoticon_features = all_emoticon_features(author)
        pos_tag_all_features = pos_tag.pos_tag_all_features(author)  # list
        aggregated_word_count_and_entropy = word_all_features(author)  # list

        features_user.extend(pos_tag_all_features)
        features_user.extend(aggregated_word_count_and_entropy)
        features_user.extend(emoticon_features)
        features_user.extend(hashtags_3(author))
        features_user.extend(user_mentions_3(author))

        if lang == 'es':
            sentiment = sentiment_analysis.analyse_author(author)
            features_user.extend(sentiment)

        features.append(features_user)
        i+=1
        print(i)

    return features
