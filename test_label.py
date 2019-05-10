from os.path import join, exists
from os import makedirs
from pickle import load
from time import time
from numpy import array
from shutil import rmtree
import operator
import re
import pickle
import numpy as np
from giovanniScripts.dataset_parser import parse_tweets_from_dir
from utils import abort_clean


from giovanniScripts.classifiers import get_classifier
from giovanniScripts.features import get_features_extr
from giovanniScripts.persistance import save_scores, save_model, save_author_file
from giovanniScripts.pipeline import get_pipeline
from giovanniScripts.utils import build_corpus, abort_clean, print_scores, format_dir_name
from giovanniScripts.utils import get_classifier_name, get_features_extr_name, get_labels
from giovanniScripts import clean_ar, clean_en, clean_es
import giovanniScripts.generic_features_text as generic
import giovanniScripts.specific_features_en as specific_en
import giovanniScripts.specific_features_es as specific_es

from sklearn.base import clone
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.model_selection import KFold

from giovanniScripts import clean_en_txt_word2vec, clean_es_txt  # Alaa : for tweet2vec
from tweet2vec import load_vectors, tweet2vec

options = {
    'text_clf_path_tfidf': "./output_txt_train/tfidf",
    'text_clf_path_label': './output_txt_train/label',
    'text_clf_path_meta': './output_txt_train/meta',
    'text_clf_path_bot': './output_txt_train/bot',
    'text_clf_path_user2vec': './output_txt_train/user2vec'
}


def parse_gender_dict(truthFilePath):
    with open(truthFilePath) as f:
        content = f.readlines()
        content = [x.strip() for x in content]

    genders = dict()
    # Female label is 0 ; Male label is 1
    for author_info in content:
        infos = author_info.split(':::')
        current_author_gender = None
        if(infos[1] == 'female'):
            current_author_gender = 0
        else:
            current_author_gender = 1
        genders[infos[0]] = current_author_gender

    return genders


def parse_gender_dict_2019(truthFilePath):
    with open(truthFilePath) as f:
        content = f.readlines()
        content = [x.strip() for x in content]

    genders = dict()
    # Female label is 0 ; Male label is 1
    for author_info in content:
        infos = author_info.split(':::')
        current_author_gender = None
        if infos[1] == 'bot':
            current_author_gender = 2
        else:
            if(infos[2] == 'female'):
                current_author_gender = 0
            else:
                current_author_gender = 1
        genders[infos[0]] = current_author_gender

    return genders


def predict(input_path,  output_path, lang="es", verbosity_level=1):

    Authors_full = parse_tweets_from_dir(
        input_dir=format_dir_name(input_path + "/" + lang + "/"),
        aggregation=1,
        label=False,
        verbosity_level=verbosity_level,
        remove_URL_and_mention=True)

    i = 0
    Authors = []
    while i < 100:
        Authors.append(Authors_full[i])
        i = i + 1

    with open(options['text_clf_path_label'] + '/' + lang + '/label-classifier.p', "rb") as input_file:
        clf_label = pickle.load(input_file)

    generic_features_test = generic.all_generic_features(Authors)
    specific_features_test = []
    if lang == 'en':
        specific_features_test = specific_en.get_all_specific_features(
            Authors)
    if lang == 'es':
        specific_features_test = specific_es.get_all_specific_features_label(
            Authors)
    i = 0
    for author in Authors:
        print(i)
        features = generic_features_test[i] + specific_features_test[i]
        print(len(features))
        prediction_author = clf_label.predict_proba([features])


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", help="Path to the whole dataset")
    parser.add_argument(
        "-o", help="Path to save the result of the prediction as xml files")
    parser.add_argument(
        "-l", help="Path to save the result of the prediction as xml files")

    args = parser.parse_args()

    predict(input_path=args.i,
            output_path=args.o, lang=args.l, verbosity_level=0)
