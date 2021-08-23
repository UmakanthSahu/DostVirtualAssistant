from nltk import word_tokenize
from numpy import zeros,float32
from nltk.stem.porter import PorterStemmer

stemmer  = PorterStemmer()

def tokenize(sentence):
    return word_tokenize(sentence)

def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence,all_words):
    tokenized_sentence = [stem(w) for w in tokenized_sentence]

    bag = zeros(len(all_words), dtype=float32)

    for index,w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[index] = 1.0

    return bag
    '''
    arr  = [ 0  for _ in all_words]
    for word in tokenized_sentence:
        if word in all_words:
            arr[all_words.index(word)] = 1
    return arr
    '''

#words = ["hi", "hello", "i","you","bye","thanks","cool"]
#sentence = ["hello","how","are","you"]
#print(bag_of_words(sentence,words))

'''
words =  tokenize("How’s the weather likely today?")
#["organize","organizes","organizing","organs"]
stemmed_words = [ stem(w) for w in words]
print(stemmed_words)
'''