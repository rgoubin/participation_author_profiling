import giovanniScripts.clean_en as clean_en
import re
import emojis


def emoji_1(Authors):
    for author in Authors:
        emoji = 0
        for tweet in author['tweets']:
            emoji = emoji + emojis.count(tweet)
            '''emoji = emoji + 
                len(re.findall(u'[\U0001f600-\U0001f650]',
                               tweet))'''
        author['emoji'] = emoji


def emoji_2(Authors):
    features = []
    for author in Authors:
        emoji = 0
        for tweet in author['tweets']:
            emoji = emoji + emojis.count(tweet)
            '''emoji = emoji + 
                len(re.findall(u'[\U0001f600-\U0001f650]',
                               tweet))'''
        features.append(emoji)

    return features


def first_person_1(Authors):
    for author in Authors:
        first_person = 0
        for tweet in author['tweets']:
            current_preprocessed_tweet = clean_en.tokenize(tweet)
            first_person = first_person + \
                current_preprocessed_tweet.count('<first_person>')
        author['first_person'] = first_person


def first_person_2(Authors):
    features = []
    for author in Authors:
        first_person = 0
        for tweet in author['tweets']:
            current_preprocessed_tweet = clean_en.tokenize(tweet)
            first_person = first_person + \
                current_preprocessed_tweet.count('<first_person>')
        features.append(first_person)

    return features


def pronouns_1(Authors):
    for author in Authors:
        pronouns = 0
        for tweet in author['tweets']:
            current_preprocessed_tweet = clean_en.tokenize(tweet)
            pronouns = pronouns + current_preprocessed_tweet.count('<pronoun>')
        author['pronouns'] = pronouns


def pronouns_2(Authors):
    features = []
    for author in Authors:
        pronouns = 0
        for tweet in author['tweets']:
            current_preprocessed_tweet = clean_en.tokenize(tweet)
            pronouns = pronouns + current_preprocessed_tweet.count('<pronoun>')
        features.append(pronouns)

    return features


def negations_1(Authors):
    for author in Authors:
        negations = 0
        for tweet in author['tweets']:
            current_preprocessed_tweet = clean_en.tokenize(tweet)
            negations = negations + \
                current_preprocessed_tweet.count('<negation>')
        author['negations'] = negations


def negations_2(Authors):
    features = []
    for author in Authors:
        negations = 0
        for tweet in author['tweets']:
            current_preprocessed_tweet = clean_en.tokenize(tweet)
            negations = negations + \
                current_preprocessed_tweet.count('<negation>')
        features.append(negations)

    return features


def get_all_specific_features(Authors):
    features = []
    for author in Authors:
        features_user = []
        emoji = 0
        first_person = 0
        pronouns = 0
        negations = 0
        for tweet in author['tweets']:
            current_preprocessed_tweet = clean_en.tokenize(tweet)
            emoji = emoji + emojis.count(tweet)
            '''emoji = emoji + 
                len(re.findall(u'[\U0001f600-\U0001f650]',
                               tweet))'''
            first_person = first_person + \
                current_preprocessed_tweet.count('<first_person>')
            pronouns = pronouns + current_preprocessed_tweet.count('<pronoun>')
            negations = negations + \
                current_preprocessed_tweet.count('<negation>')

        features_user.append(emoji)
        features_user.append(first_person)
        features_user.append(pronouns)
        features_user.append(negations)
        features.append(features_user)

    return features


def get_all_specific_features_label(Authors):
    features = []
    print("specific features")
    i = 0
    for author in Authors:
        print(i)
        i = i + 1
        features_user = []
        emoji = 0
        first_person = 0
        pronouns = 0
        negations = 0
        for tweet in author['tweets']:
            current_preprocessed_tweet = clean_en.tokenize(tweet)
            emoji = emoji + emojis.count(tweet)
            '''emoji = emoji + 
                len(re.findall(u'[\U0001f600-\U0001f650]',
                               tweet))'''
            first_person = first_person + \
                current_preprocessed_tweet.count('<first_person>')
            pronouns = pronouns + current_preprocessed_tweet.count('<pronoun>')
            negations = negations + \
                current_preprocessed_tweet.count('<negation>')

        '''features_user.append(emoji)
        features_user.append(first_person)
        features_user.append(pronouns)'''
        features_user.append(negations)
        features.append(features_user)

    return features
