# coding=utf-8
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.stem import SnowballStemmer


class clean_es_txt:

    punctuations_list = string.punctuation+'¿'+'¡'
    stopwords_list = stopwords.words('spanish')

    first_person = ['mí', 'mi', 'mis', 'mío', 'mía', 'míos', 'mías', 'mio', 'mia', 'mios', 'mias', 'yo',
                    'nos', 'nuestro', 'nuestra', 'nuestros', 'nuestras']

    pronouns = ['tú', 'tu', 'te', 'ti', 'tu', 'tus', 'ellas', 'ella', 'vosostros', 'vosostras', 'os',
                'tuyo', 'tuya', 'tuyos', 'tuyas', 'suyo', 'suya', 'suyos', 'suyas', 'vuestro', 'vuestra', 'vuestros',
                'vuestras']

    negation = ['no']

    def __init__(self):
        pass

    def normalize(self, text):
        return text

    def remove_punctuations(self, text):
        translator = str.maketrans('', '', clean_es_txt.punctuations_list)
        return text.translate(translator)

    def remove_repeating_char(self, text):
        return re.sub(r'(.)\1+', r'\1', text)

    def label_stopwords(self, text):
        for word in clean_es_txt.first_person:
            text = text.replace(' ' + word + ' ', ' <first_person> ')
        for word in clean_es_txt.pronouns:
            text = text.replace(' ' + word + ' ', ' <pronoun> ')
        for word in clean_es_txt.negation:
            text = text.replace(' ' + word + ' ', ' <negation> ')
        # print(text)
        return text

    def tokenize(self, text):
        text = self.remove_punctuations(text)
        text = self.label_stopwords(text)
        #text = self.normalize(text)
        text = self.remove_repeating_char(text)
        tokenizer = TweetTokenizer()
        tokens = tokenizer.tokenize(text)
        filtered_tokens = []
        for token in tokens:
            if token not in clean_es_txt.stopwords_list:
                filtered_tokens.append(token)
        return filtered_tokens
        # return text.split()
