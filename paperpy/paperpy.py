#!/usr/bin/python
# -*- coding: utf8 -*-

# This program is free software licenced under MIT Licence.
# You can find a copy of this licence in the LICENSE file in the top directory of source code.

"""
This script analyses a text for proofreading.
Better description will follow :P
"""

import sys
import pypandoc    # <- Needs pandoc installed
from textblob import TextBlob
from tabulate import tabulate

def main(argv):
    """
    Reads in the filepath and starts analysis.
    """
    if len(argv) > 1:
        # Input via arguments
        # TODO: Doesn't work yet
        filepath = str(argv[1:])
    else:
        # Input via console
        if sys.version_info[0] < 3:    # <- python 2
            filepath = str(raw_input("Filepath: "))
        else:
            filepath = str(input("Filepath: "))

    # Settings
    language = 'de'

    # Data paths
    attentionfile = 'data/' + language + '/attentionwords.txt'
    ngramfile = 'data/' + language + '/ngramlist.txt'

    # Test path
    # filepath = '../tests/test.docx'

    # Load textfile and convert to plain text
    text = pypandoc.convert_file(filepath, 'plain')

    # Load attentionwords as list
    attentionwords = open(attentionfile, encoding='utf-8').read().splitlines()

    # Load ngramlist as list
    ngramlist = open(ngramfile, encoding='utf-8').read().splitlines()

    # Create a textblob to work with
    blob = TextBlob(text)

    # Contains all the words
    wordlist = blob.words

    # Unordered set (unique words)
    wordset = list(set(wordlist))

    # Contains all the sentences
    sentences = blob.sentences

    # Contains all the ngrams
    ngrams = blob.ngrams(n=2)

    ## Print all the sentences
    #for sentence in sentences:
    #   print(sentence)

    # create wordtable
    wordtable = []
    for word in wordset:
        wordtable.append([word, str(wordlist.count(word)), str(blob.find(word))])

    # sort by amount
    wordtable = sorted(wordtable, key=lambda word: int(word[1]), reverse=True)

    # print amount table
    print(tabulate(wordtable))

    print("\n")

    # print attentionswords list and position where found in text
    attentiontable = []
    for word in attentionwords:
        attentiontable.append([word, str(blob.find(word))])

    # sort by position
    attentiontable = sorted(attentiontable, key=lambda word: int(word[1]))

    # print amount table
    print(tabulate(attentiontable))

    print("\n")

    # print the ngrams which are intersting
    phrasetable = []
    for ngram in ngrams:
        if (ngram[0].lower() == ngram[1].lower()) | (ngram[0].lower() in ngramlist):
            phrase = ' '.join(str(word) for word in ngram)
            phrasetable.append([phrase, str(blob.find(phrase))])

    # sort by position
    phrasetable = sorted(phrasetable, key=lambda word: int(word[1]))

    # print amount table
    print(tabulate(phrasetable))

    print("\n")

# Execute only if run as a script
if __name__ == "__main__":
    main(sys.argv)
