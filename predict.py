from os.path import join, exists
from os import makedirs
from pickle import load
from time import time
from numpy import array
from shutil import rmtree
import re
import pickle

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

options = {
    'text_clf_path_tfidf': "./output_txt_train/tfidf",
    'text_clf_path_label': './output_txt_train/label',
    'text_clf_path_meta': './output_txt_train/meta',
    'text_clf_path_bot': './output_txt_train/bot',
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
        if infos[1] == 'bot':
            current_author_gender = 2
        else:
            if(infos[2] == 'female'):
                current_author_gender = 0
            else:
                current_author_gender = 1
        genders[infos[0]] = current_author_gender

    return genders


def save_xmls(output_path, lang, predictions_dict):
    if exists(output_path) == False:
        makedirs(output_path)

    for prediction in predictions_dict:
        author = dict()
        author['id'] = prediction
        author['lang'] = lang
        if predictions_dict[prediction] == 'bot':
            author['type'] = 'bot'
        else:
            author['type'] = 'human'
        author['gender'] = predictions_dict[prediction]
        save_author_file(
            author=author, output_dir=output_path + '/', verbose=0)


def predict(input_path,  output_path, verbosity_level=1):
    '''

    For each language, proceeds as follow:
        - takes in input the corresponding .pkl file
        - train a text-based classifier on the 80% split
        - save the resulting model in outputPath

    :param inputPath:  Path to PAN19 dataset
    :param splitsPath: Path to dir containing the .pkl files produced by 'splitting.py'
    :param outputPath: Path to dir in which the outputs models will be saved
        NB. Create outputPath directory before using this function
    '''

    for lang in ['en', 'es']:

        input_dir = join(input_path, lang)
        output_dir = join(output_path, lang)

        from sklearn.svm import LinearSVC
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import cross_val_score
        from sklearn.calibration import CalibratedClassifierCV

        print("Extracting Authors:")

        Authors = parse_tweets_from_dir(
            input_dir=format_dir_name(input_path + "/" + lang + "/"),
            aggregation=1,
            label=False,
            verbosity_level=verbosity_level,
            remove_URL_and_mention=True)

        predictions_dict = dict()
        Bots = []
        Humans = []
        # TO DELETE
        # Humans = Authors

        Bots = Authors

        # -----------------------------------------------------
        # ------ DETERMINING IF USERS ARE BOTS OR HUMANS ------
        # -----------------------------------------------------

        print('Get bot classifier')
        clf_bot = None
        with open(options['text_clf_path_bot'] + '/' + lang + '/bot-classifier.p', "rb") as input_file:
            clf_bot = pickle.load(input_file)

        print('--------------- feature extractor ------------------')
        bot_features_test = generic.all_generic_bot_features(Bots)

        '''specific_features_test = []
        if lang == 'en':
            specific_features_test = specific_en.get_all_specific_features(
                Bots)
        if lang == 'es':
            specific_features_test = specific_es.get_all_specific_features(
                Bots)'''
        print('--------------- feature extracted ------------------')
        bot_predictions_label = dict()

        print('--------------- construction of features for the bot classifier ------------------')
        i = 0
        for author in Bots:
            prediction_author = clf_bot.predict_proba([bot_features_test[i]])

            if prediction_author[0][1] >= 0.5:
                # predictions_dict[author['id']] = 'human'
                Humans.append(author)
            else:
                predictions_dict[author['id']] = 'bot'
            i = i + 1

        print("--------------- bot prediction done ---------------")
        #save_xmls(output_path + '/' + lang, lang, predictions_dict)


        # -----------------------------------------------------
        # --- DETERMINING IF THE HUMANS ARE FEMALE OR MALE ----
        # -----------------------------------------------------

        print('Get classifiers label and meta')
        clf_label = None
        clf_meta = None
        with open(options['text_clf_path_label'] + '/' + lang + '/label-classifier.p', "rb") as input_file:
            clf_label = pickle.load(input_file)
        with open(options['text_clf_path_meta'] + '/' + lang + '/meta-classifier.p', "rb") as input_file:
            clf_meta = pickle.load(input_file)

        import text_prediction
        predictions_test_tfidf = text_prediction.predict(
            input_path, options['text_clf_path_tfidf'], languages=[lang])

        print('--------------- feature extractor ------------------')
        generic_features_test = generic.all_generic_features(Humans)
        specific_features_test = []
        if lang == 'en':
            specific_features_test = specific_en.get_all_specific_features(
                Humans)
        if lang == 'es':
            specific_features_test = specific_es.get_all_specific_features(
                Humans)
        print('--------------- feature extracted ------------------')
        text_predictions_label = dict()

        print('--------------- construction of features for the meta classifier ------------------')
        X_test = dict()
        i = 0
        for author in Humans:
            features = generic_features_test[i] + specific_features_test[i]
            prediction_author = clf_label.predict_proba([features])
            text_predictions_label[author['id']] = prediction_author[0]

            i = i + 1

            toAppend = []
            toAppend.append(predictions_test_tfidf[author['id']][0])
            toAppend.append(predictions_test_tfidf[author['id']][1])
            toAppend.append(prediction_author[0][0])
            toAppend.append(prediction_author[0][1])

            X_test[author['id']] = toAppend
        X_test_casted = dict()

        for author in Humans:
            x = X_test[author['id']]
            toAppend = []
            for feature in x:
                toAppend.append(float(feature))
            X_test_casted[author['id']] = toAppend

        print('--------------- meta classifier predictions ------------------')
        i = 0
        for author in Humans:
            prediction_author = clf_meta.predict_proba(
                [X_test_casted[author['id']]])
            if prediction_author[0][0] >= 0.5:
                predictions_dict[author['id']] = 'female'
            else:
                predictions_dict[author['id']] = 'male'
            i = i + 1

        print('--------------- meta classifier predictions done ------------------')

        print('--------------- saving ------------------')
        save_xmls(output_path + '/' + lang, lang, predictions_dict)


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", help="Path to the whole dataset")
    parser.add_argument(
        "-o", help="Path to save the result of the prediction as xml files")

    args = parser.parse_args()

    predict(input_path=args.i,
            output_path=args.o, verbosity_level=0)
