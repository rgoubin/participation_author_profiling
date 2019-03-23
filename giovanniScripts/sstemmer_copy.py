# -*- coding: utf-8 -*-
#
# Natural Language Toolkit: S-Stemmer
#
# Author: J. Savoy
# Algorithms: Donna Harman.  How effective is suffixing?
#      Journal of the American Society for Information Science
#      42(1), 1991, p. 7-15
# 
# URL: <http://nltk.org/>


"""
S-Stemmer
The S-Stemmer is a light English stemmer that is based on removing the suffixes
from the word related to the plural form.
This stemmer is not
based on any dictionary and can be used on-line effectively.
"""
from __future__ import unicode_literals
import re

from nltk.stem.api import StemmerI


class SStemmer(StemmerI):
    '''
    The S-Stemmer is a light English stemmer that is based on removing the suffixes
    from the word related to the plural form.
    '''

    def __init__(self):
        self.min = 0

    def stem(self, token):
        """
            call this function to get the word's stem based on S-Stemmer.
        """
        try:
            aLen = len(token)-1
            if (token is None) or (aLen < self.min):
                raise ValueError(
                    "The word could not be stemmed, because it is empty or too small !")
# Min word size = 4 letters            
            if (aLen <= 2):
                return token
# Must ends with -s
            if (token[aLen] != u's'):
                return token
# Rule 1  ending in -ies
            if (token[aLen-1] == u'e') and (token[aLen-2] == u'i'):
                if ((token[aLen-3] != u'e') and (token[aLen-3] != u'a')):
                    return (token[:aLen-2]+u'y')
                else:
                    return token
# Rule 2  ending in -es
            if (token[aLen-1] == u'e'):
                if ((token[aLen-2] != u'a') and (token[aLen-2] != u'e') and (token[aLen-2] != u'o')):
                    return token[:aLen]
                else:
                    return token
# Rule 3 ending in -s           
            if ((token[aLen-1] != u'u') and (token[aLen-1] != u's')):
                return token[:aLen]
            else:
                return token
        except ValueError as e:
            print(e)

    def __repr__(self):
        return '<SStemmer>'


