import xml.etree.ElementTree as ET

xmls_path = '../../xml'
dataset_path = '../../PAN2018-AP-Train/pan19-author-profiling-training-2019-01-28'


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
            current_author_gender = 'bot'
        else:
            if(infos[2] == 'female'):
                current_author_gender = 'female'
            else:
                current_author_gender = 'male'
        genders[infos[0]] = current_author_gender

    return genders


def check_xml():

    for lang in ['en', 'es']:
        bool_all_attrib = True
        bool_coherence = True
        number_of_bots = 0
        number_of_humans = 0
        number_of_good_gender_predictions = 0
        number_of_good_type_prediction = 0
        dict_language = parse_gender_dict(
            dataset_path + '/' + lang + '/truth.txt')
        for author in dict_language:
            tree = ET.parse(xmls_path + '/' + lang + '/' + author + '.xml')
            root = tree.getroot()
            if ('lang' not in root.attrib) or ('type' not in root.attrib) or ('gender' not in root.attrib):
                bool_all_attrib = False
            if (root.attrib['type'] == 'bot') and (root.attrib['gender'] != 'bot'):
                bool_coherence = False
            if (root.attrib['type'] == 'human') and ((root.attrib['gender'] != 'female') and (root.attrib['gender'] != 'male')):
                bool_coherence = False

            if dict_language[root.attrib['id']] == 'bot':
                number_of_bots = number_of_bots + 1
                if root.attrib['type'] == 'bot':
                    number_of_good_type_prediction = number_of_good_type_prediction + 1
                if root.attrib['gender'] == 'bot':
                    number_of_good_gender_predictions = number_of_good_gender_predictions + 1

            if dict_language[root.attrib['id']] == 'female':
                number_of_humans = number_of_humans + 1
                if root.attrib['type'] == 'human':
                    number_of_good_type_prediction = number_of_good_type_prediction + 1
                if root.attrib['gender'] == 'female':
                    number_of_good_gender_predictions = number_of_good_gender_predictions + 1

            if dict_language[root.attrib['id']] == 'male':
                number_of_humans = number_of_humans + 1
                if root.attrib['type'] == 'human':
                    number_of_good_type_prediction = number_of_good_type_prediction + 1
                if root.attrib['gender'] == 'male':
                    number_of_good_gender_predictions = number_of_good_gender_predictions + 1

        print('Language:' + lang.upper())
        print('bool_all_attrib: ' + str(bool_all_attrib))
        print('bool_coherence: ' + str(bool_coherence))
        print('number_of_good_type_prediction: ' +
              str(number_of_good_type_prediction))
        print('number_of_good_gender_predictions: ' +
              str(number_of_good_gender_predictions))
        print('number_of_bots: ' + str(number_of_bots))
        print('number_of_humans: ' + str(number_of_humans))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", help="Path to the whole dataset")
    parser.add_argument(
        "-o", help="Path to save the result of the prediction as xml files")

    args = parser.parse_args()
    xmls_path = args.i
    dataset_path = args.o
    check_xml()
