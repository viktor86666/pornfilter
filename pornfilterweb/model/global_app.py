__author__ = 'rama'
__date__ = '5/29/2015'

class VarGlobal:

    # nama kelas untuk kelas negatif dan kelas positif
    NEGATIVE_CLASS = "porno"
    POSITIVE_CLASS = "tidak-porno"

    # variabel untuk menyimpan string bahasa
    ENGLISH = "english"
    INDONESIA = "indonesia"

    # direktori penyimpanan model vectorizer
    IDN_VECTORIZER_PATH = "res/model/idn_vectorizer.pkl"
    ENG_VECTORIZER_PATH = "res/model/eng_vectorizer.pkl"

    # direktori penyimpanan model classifier
    IDN_CLASSIFIER_MODEL_PATH = "res/model/idn_classifier.pkl"
    ENG_CLASSIFIER_MODEL_PATH = "res/model/eng_classifier.pkl"

    # direktori penyimpanan file data training
    IDN_DOCS_TRAIN_PATH = "res/data-training/data-training-indo.txt"
    ENG_DOCS_TRAIN_PATH = "res/data-training/data-training-eng.txt"

    # direktori penyimpanan file stopword
    IDN_STOPWORD_PATH = "res/stopword/stoplist-ind.txt"
    ENG_STOPWORD_PATH = "res/stopword/stoplist-eng.txt"