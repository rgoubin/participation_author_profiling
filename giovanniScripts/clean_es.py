# coding=utf-8
import re
import string
from nltk.corpus import stopwords

punctuations_list = string.punctuation+'¿'+'¡'
stopwords_list = stopwords.words('spanish')

first_person = ['mí', 'mi', 'mis', 'mío', 'mía', 'míos', 'mías', 'mio', 'mia', 'mios', 'mias', 'yo',
                'nos', 'nuestro', 'nuestra', 'nuestros', 'nuestras']

pronouns = ['tú', 'tu', 'te', 'ti', 'tu', 'tus', 'ellas', 'ella', 'vosostros', 'vosostras', 'os',
            'tuyo', 'tuya', 'tuyos', 'tuyas', 'suyo', 'suya', 'suyos', 'suyas', 'vuestro', 'vuestra', 'vuestros',
            'vuestras']

negation = ['no']

stopwords_list_2 = ['de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 'con',
                    'no', 'una', 'su', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 'este', 'sí', 'porque',
                    'esta', 'entre', 'cuando', 'muy', 'sin', 'sobre', 'también', 'me', 'hasta', 'hay', 'donde', 'quien',
                    'desde', 'todo', 'nos', 'durante', 'todos', 'uno', 'les', 'ni', 'contra', 'otros', 'ese', 'eso', 'ante',
                    'ellos', 'e', 'esto', 'mí', 'antes', 'algunos', 'qué', 'unos', 'yo', 'otro', 'otras', 'otra', 'él',
                    'tanto', 'esa', 'estos', 'mucho', 'quienes', 'nada', 'muchos', 'cual', 'poco', 'ella', 'estar', 'estas',
                    'algunas', 'algo', 'nosotros', 'mi', 'mis', 'tú', 'te', 'ti', 'tu', 'tus', 'ellas', 'nosotras',
                    'vosostros', 'vosostras', 'os', 'mío', 'mía', 'míos', 'mías', 'tuyo', 'tuya', 'tuyos', 'tuyas', 'suyo',
                    'suya', 'suyos', 'suyas', 'nuestro', 'nuestra', 'nuestros', 'nuestras', 'vuestro', 'vuestra', 'vuestros',
                    'vuestras', 'esos', 'esas', 'estoy', 'estás', 'está', 'estamos', 'estáis', 'están', 'esté', 'estés',
                    'estemos', 'estéis', 'estén', 'estaré', 'estarás', 'estará', 'estaremos', 'estaréis', 'estarán',
                    'estaría', 'estarías', 'estaríamos', 'estaríais', 'estarían', 'estaba', 'estabas', 'estábamos',
                    'estabais', 'estaban', 'estuve', 'estuviste', 'estuvo', 'estuvimos', 'estuvisteis', 'estuvieron',
                    'estuviera', 'estuvieras', 'estuviéramos', 'estuvierais', 'estuvieran', 'estuviese', 'estuvieses',
                    'estuviésemos', 'estuvieseis', 'estuviesen', 'estando', 'estado', 'estada', 'estados', 'estadas',
                    'estad', 'he', 'has', 'ha', 'hemos', 'habéis', 'han', 'haya', 'hayas', 'hayamos', 'hayáis', 'hayan',
                    'habré', 'habrás', 'habrá', 'habremos', 'habréis', 'habrán', 'habría', 'habrías', 'habríamos',
                    'habríais', 'habrían', 'había', 'habías', 'habíamos', 'habíais', 'habían', 'hube', 'hubiste', 'hubo',
                    'hubimos', 'hubisteis', 'hubieron', 'hubiera', 'hubieras', 'hubiéramos', 'hubierais', 'hubieran',
                    'hubiese', 'hubieses', 'hubiésemos', 'hubieseis', 'hubiesen', 'habiendo', 'habido', 'habida', 'habidos',
                    'habidas', 'soy', 'eres', 'es', 'somos', 'sois', 'son', 'sea', 'seas', 'seamos', 'seáis', 'sean',
                    'seré', 'serás', 'será', 'seremos', 'seréis', 'serán', 'sería', 'serías', 'seríamos', 'seríais',
                    'serían', 'era', 'eras', 'éramos', 'erais', 'eran', 'fui', 'fuiste', 'fue', 'fuimos', 'fuisteis',
                    'fueron', 'fuera', 'fueras', 'fuéramos', 'fuerais', 'fueran', 'fuese', 'fueses', 'fuésemos', 'fueseis',
                    'fuesen', 'sintiendo', 'sentido', 'sentida', 'sentidos', 'sentidas', 'siente', 'sentid', 'tengo',
                    'tienes', 'tiene', 'tenemos', 'tenéis', 'tienen', 'tenga', 'tengas', 'tengamos', 'tengáis', 'tengan',
                    'tendré', 'tendrás', 'tendrá', 'tendremos', 'tendréis', 'tendrán', 'tendría', 'tendrías', 'tendríamos',
                    'tendríais', 'tendrían', 'tenía', 'tenías', 'teníamos', 'teníais', 'tenían', 'tuve', 'tuviste', 'tuvo',
                    'tuvimos', 'tuvisteis', 'tuvieron', 'tuviera', 'tuvieras', 'tuviéramos', 'tuvierais', 'tuvieran',
                    'tuviese', 'tuvieses', 'tuviésemos', 'tuvieseis', 'tuviesen', 'teniendo', 'tenido', 'tenida', 'tenidos',
                    'tenidas', 'tened']


def normalize(text):
    return text


def remove_punctuations(text, do_label=True):
    punctuations_list_filtered = punctuations_list
    if do_label:
        punctuations_list_filtered = punctuations_list.replace('#', '')
        punctuations_list_filtered = punctuations_list_filtered.replace(
            '@', '')
        punctuations_list_filtered = punctuations_list_filtered.replace(
            '\'', '')

    translator = str.maketrans('', '', punctuations_list)
    return text.translate(translator)


def label_stopwords(text):
    for word in first_person:
        text = text.replace(' ' + word + ' ', ' <first_person> ')
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
    # print(text)
    mention_re = re.compile(
        "(?:^|\s)[@@]{1}([^\s#<>[\]|{}]+)", re.UNICODE)
    list_mentions = set(mention_re.findall(text))
    #print('list mention')
    # print(list_mentions)
    for mention in list_mentions:
        text = text.replace('@' + mention, ' <user_mention> ')

    return text


def remove_repeating_char(text, do_label=True):
    return re.sub(r'(.)\1+', r'\1', text)


def tokenize(text, do_label=True):
    # print('------------------------------------------')
    # print(text)
    text = remove_punctuations(text, do_label)
    if do_label:
        text = label_user_mentions(text)
        text = label_hashtag(text)
        text = label_stopwords(text)

    text = remove_repeating_char(text)
    # print('------------------------------------------')
    # print(text)
    # print('------------------------------------------')
    return text
