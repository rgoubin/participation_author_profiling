import csv
import pickle
from os.path import join, exists
from os import makedirs
from shutil import rmtree


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


def test(options):

    with open(options['user2vec_path'], 'rb') as user2vec_file:
        user_vectors = pickle.load(user2vec_file)

    gender_dict_test = parse_gender_dict_2019(
        options['dataset_path'] + '/truth.txt')

    print(len(user_vectors))

    print(len(gender_dict_test))

    X = []
    y = []

    X_test = []
    y_test = []

    print("Spliting of data")

    for user in user_vectors:
        if (user in gender_dict_test) and (gender_dict_test[user] != 2):
            X_test.append(user_vectors[user])
            y_test.append(gender_dict_test[user])

    print("Data splitted")

    from sklearn.svm import LinearSVC
    from sklearn.calibration import CalibratedClassifierCV

    svm = LinearSVC(random_state=0)
    clf = CalibratedClassifierCV(svm)

    print("Training on " + str(len(X)) + " users")

    clf.fit(X, y)

    print("Testing on " + str(len(X_test)) + " users")

    score = clf.score(X_test, y_test)

    print("score :")
    print(score)

    if exists('./output_txt_train/user2vec' + '/' + options['languages']):
        rmtree('./output_txt_train/user2vec' + '/' + options['languages'])
    makedirs('./output_txt_train/user2vec' + '/' + options['languages'])
    pickle.dump(clf, open('./output_txt_train/user2vec' + '/' +
                          options['languages'] + '/user2vec-classifier.p', "wb"))


def predict(dict_users, clf_path, csv_file):

    prediction_dict = dict()

    with open(clf_path + '/user2vec-classifier.p', "rb") as clf_file:
        clf = pickle.load(clf_file)

    with open(options['user2vec_path'], 'rb') as user2vec_file:
        user_vectors = pickle.load(user2vec_file)

    for user in user_vectors:
        if (user in dict_users) and (dict_users[user] != 2):
            prediction_user = clf.predict_proba([user_vectors[user]])
            prediction_dict[user] = prediction_user

    return prediction_user


if __name__ == "__main__":
    options = {
        'languages': 'en'
    }

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", help="Path to the user2vec file")
    parser.add_argument("-d", help="Path to the pan dataset")
    parser.add_argument("-l", help="language to test")

    args = parser.parse_args()

    if args.i is not None:
        options['user2vec_path'] = args.i

    if args.l is not None:
        options['languages'] = args.l

    if args.d is not None:
        options['dataset_path'] = args.d

    test(options)
