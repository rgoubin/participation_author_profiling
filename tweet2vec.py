from giovanniScripts import clean_en_txt, clean_es_txt
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import os, csv , io




def load_vectors(fname):
    print('Loading vectors ... ')
    fin = io.open(fname, 'r', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    for line in fin:
        tokens = line.rstrip().split(' ')
        ''' 
         print ("tokens are ", tokens ) 
        ('tokens are ', ['link', '0.0526', '0.1061', '-0.0083', '0.0913', '0.0443',...., '0.0270']) '''

        data[tokens[0]] = map(float, tokens[1:])
    print('Loading vectors Done')
    return data



def tweet2vec(wordVec, clean_tweet_tokens):

    '''
    :param wordVec: a dictionary for the word: vector
    :param tweet: the author tweet to be vectorized
    tfidf
    :return: the tweet vector which is  >>>in our supposition >>>>the  average of word2vec vectors multiplied by the word tfIdf
    '''


    foundwords= 0
    sum =[0]*300  #vector of zeors in dimention of
    words_count = len(clean_tweet_tokens)
    print('words_count', words_count)

    for word in clean_tweet_tokens:
       #wrd = word.encode("utf-8")
       wrd=word
       try:
           print(wrd)
           w_vec = wordVec[wrd]

           w_vec = list(w_vec)
           print("word found with a value ", w_vec)
           if (len(w_vec) != 0):
               foundwords += 1
               sum = np.sum([sum, w_vec], axis=0)
               print('cur sum', sum)
       except KeyError:
            print(wrd, "does not exist in the words vectors !!!")
            continue


    #average
    if(foundwords > 0):
        avg = [x / foundwords for x in sum]  # average over found vectors
    else:
        avg=[0] * 300
    return avg , words_count , foundwords




####=======================================================================================

def tfIdf_weighted_tweet2vec(wordVec, clean_tweet_tokens, user_word_tfIdf):
    '''
    :param wordVec: a dictionary for the word: vector
    :param tweet: the author tweet to be vectorized
    tfidf
    :return: the tweet vector which is  >>>in our supposition >>>>the  average of word2vec vectors multiplied by the word tfIdf
    '''

    foundwords = 0
    sum = [0] * 300  # vector of zeors in dimention of 300 = word vector dim

    words_count = len(clean_tweet_tokens)
    print('words_count', words_count)
    for word in clean_tweet_tokens:
        # wrd = word.encode("utf-8")
        wrd = word
        try:
            print(wrd)
            w_vec = wordVec[wrd]
            w_vec = list(w_vec)
            print("word found with a value " , w_vec)
            if (len(w_vec) != 0):
                foundwords += 1
                #multiply by tfIdf
                wrd_tfIdf=  user_word_tfIdf[wrd]

                w_vec= [ i* wrd_tfIdf for i in w_vec]

                sum = np.sum([sum, w_vec], axis=0)

                #print('cur sum', sum)
        except KeyError:
            print(wrd, "does not exist in the words vectors !!!")
            continue


    # average
    if (foundwords > 0):
        avg = [x / foundwords for x in sum]  # average over found vectors
    else:
        avg = [0] * 300
    return avg, words_count, foundwords


def user_word_tfIdf(curr_author, authors):
    # each author dict contains: lang, Id, lable, tweets
    #this function will get the user tweets, rest_users_tweets : clean them : then find the tfidf for each word
        user_id = curr_author["Id"]

        user_lang = curr_author["lang"]

        word_tfIdf = {}

        if (user_lang == "en"):

            user_doc = clean_en_txt().tokenize(str(curr_author["tweets"]))

            other_users_docs = [user["tweets"] for user in authors if
                                user["Id"] != user_id and user["lang"] == "en"]
            #clean
            #other_users_docs=clean_en_txt().tokenize(str(other_users_docs)) ### too much memory

        elif (user_lang == "es"):

            other_users_docs = [user["tweets"] for user in authors if
                                user["Id"] != user_id and user["lang"] == "es"]
            user_doc = clean_es_txt().tokenize(str(curr_author["tweets"]))
            #other_users_docs = clean_es_txt().tokenize(str(other_users_docs))
        else:
            print("language", user_lang, "has not been intialized yet")

        vectorizer = TfidfVectorizer()
        response = vectorizer.fit_transform([str(user_doc), str(other_users_docs)])
        word_index=vectorizer.vocabulary_  #dict { 'car': 19, 'is': 10, 'driven': 1,......}
        #print(word_index)
        user_tfIdf_array=response.toarray()[0]#[0] is the array of user_doc

        for word,index in word_index.items():
            word_tfIdf[word] =user_tfIdf_array[index]
       #print(word_tfIdf)  {'car': 0.30814892740486904, 'is': 0.30814892740486904, 'driven': 0.30814892740486904, ,,,,}
        return word_tfIdf


def user2vec(wordVec, clean_tweets_tokens, user_word_tfIdf):

    foundwords = 0

    sum = [0] * 300  # vector of zeors in dimention of
    words_count = len(clean_tweets_tokens)
    print('words_count', words_count)
    for word in clean_tweets_tokens:
        # wrd = word.encode("utf-8")
        wrd = word
        try:

            w_vec = wordVec[wrd]
            w_vec = list(w_vec)
            if (len(w_vec) != 0):
                foundwords += 1
                # multiply by tfIdf
                wrd_tfIdf = user_word_tfIdf[wrd]
                w_vec = np.array(w_vec) * wrd_tfIdf
                sum = np.sum([sum, w_vec], axis=0)
                print('cur sum', sum)



        except KeyError:
            print(wrd, "does not exist in the words vectors !!!")
            continue



    # average
    if (foundwords > 0):
        avg = [x / foundwords for x in sum]  # average over found vectors
    else:
        avg = [0] * 300
    return avg, words_count, foundwords



#==================================================================

''' 
 if __name__ == "__main__":

    ###read the input (train) data:
    # --------------------------------
    # training_path = config.Data['train_data_path']
    training_path = "Data/pan19-author-profiling-training-2019-01-28"

    # langs = config.Data['languages']
    langs = ['en']
    authors = loadAuthors(training_path, langs)

    ### intialize the output csv file if does not exist before:
    # ------------------------------------------------------------

    
    tweet2vec_fname = "Data/simple_tweet2vec_allusers_bigfile_es_001.csv"

    exists = os.path.isfile(tweet2vec_fname)
    if (exists):
        print("output csv file already exist, will append to it!! ")
    else:
        # user2vec:
        # row=['user_Id', 'class' ,'clean_words_count',
        #       'vectorized_words_count', 'tweet_vector']

        # if Tweet2vec row is :
        row = ['user_Id', 'class', 'tweet_num', 'orginal_tweet', 'clean_tweet_tokens', 'clean_words_count',
               'vectorized_words_count', 'tweet_vector']

        with open(tweet2vec_fname, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)

    ### load fastText word vectors
    # --------------------------------

   
    word2vec_fname = "Data/fastText/cc.en.300.vec"  # English big file
    words_vectors_data = load_vectors(word2vec_fname)
    # words_vectors_data= dict()

    # tweet2vec_file = open(tweet2vec_fname, 'a')

    ###clean tweet and calculate the tweets vectors:
    # ------------------------------------------

    global_found_words = 0
    global_words_count = 0
    # tweet2vec_file.write('{')

    # if Tweet2vec :
    for x in authors:

        print('USER', x['Id'])
        tweets = x['tweets']
        lang = x["lang"]
        tweet_vec = []
        tweet_num = 0
        for orginal_tweet in tweets:
            tweet_num += 1
            print('tweet is', orginal_tweet)

            # clean the tweet
            if (lang == "en"):
                clean_tweet_tokens = clean_en_txt().tokenize(orginal_tweet)
            elif (lang == "es"):
                clean_tweet_tokens = clean_es_txt().tokenize(orginal_tweet)
            else:
                print("language", lang, "has not been initialized yet")

            ### if weighted tweet2vec:
            # author_word_tfIdf = user_word_tfIdf(x, authors)
            # tweet_vector, words_count, vectorized_words_count = tfIdf_weighted_tweet2vec(words_vectors_data,
            #                                                                             clean_tweet_tokens,
            #                                                                            author_word_tfIdf)

            # else
            tweet_vector, words_count, vectorized_words_count = tweet2vec(words_vectors_data, clean_tweet_tokens)

            print("tweet vector:", tweet_vector)

            global_found_words += vectorized_words_count
            global_words_count += words_count

            # write a new row for this tweet in csv file
            row = [x['Id'], x['lable'], tweet_num, orginal_tweet.encode("utf-8"), clean_tweet_tokens,
                   words_count,
                   vectorized_words_count, tweet_vector]
            with open(tweet2vec_fname, 'a') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
                print("new Row added to file")

            print("curr global_words_count", global_words_count)

            print("curr global_found_words", global_found_words)

    ratio = (float(global_found_words)) / global_words_count
    print("global ratio of founded words is", ratio)
'''