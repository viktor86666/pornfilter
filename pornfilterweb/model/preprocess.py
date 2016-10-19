__author__ = 'rama'
__date__ = '4/17/2015'

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import numbers

class Preprocess(TfidfVectorizer):
    """
    Kelas Preprocess ini diturunkan dari kelas sklearn.feature_extraction.text.CountVectorizer dari library SciKit.
    Pada kelas ini ditambahkan parameter untuk menginputkan fungsi tokenize, stemmer, ngram dengan NLTK

    Extend class TfidfVectorizer untuk menggunakan vectorizer dengan feature representation weigting TF-IDF
    atau Extends class CountVectorizer untuk menggunakan vectorizer dengan feature representation binary atau int(frekuensi)
    """
    def __init__(self, input='content', encoding='utf-8',
                 decode_error='strict', strip_accents=None,
                 lowercase=True, preprocessor=None, tokenizer=None,
                 stop_words=None, token_pattern=r"(?u)\b\w\w+\b",
                 ngram_range=(1, 1), analyzer='word',
                 max_df=1.0, min_df=1, max_features=None,
                 vocabulary=None, binary=False, dtype=np.int64, stemmer = None
    ):
        TfidfVectorizer.__init__(self)
        self.input = input
        self.encoding = encoding
        self.decode_error = decode_error
        self.strip_accents = strip_accents
        self.preprocessor = preprocessor
        self.tokenizer = tokenizer
        self.analyzer = analyzer
        self.lowercase = lowercase
        self.token_pattern = token_pattern
        self.stop_words = stop_words
        self.max_df = max_df
        self.min_df = min_df
        if max_df < 0 or min_df < 0:
            raise ValueError("negative value for max_df of min_df")
        self.max_features = max_features
        if max_features is not None:
            if (not isinstance(max_features, numbers.Integral) or
                    max_features <= 0):
                raise ValueError(
                    "max_features=%r, neither a positive integer nor None"
                    % max_features)
        self.ngram_range = ngram_range
        self.vocabulary = vocabulary
        self.binary = binary
        self.dtype = dtype
        self.stemmer = stemmer

    # def build_analyzer(self):
    #     """
    #     override fungsi build_analizer dari lib scikit-learn untuk menambahkan proses stemming
    #     :return:
    #     """
    #
    #     analyzer = super(Preprocess, self).build_analyzer()
    #     if self.stemmer:
    #         return lambda doc:(
    #             self.stemmer.stem(w)for w in analyzer(doc)
    #         )
    #     else:
    #         return lambda doc:(analyzer(doc))

