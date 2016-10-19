__author__ = 'rama'
__date__ = '4/11/2015'

from model.global_app import VarGlobal
from sklearn.externals import joblib
from model.preprocess import Preprocess
from sklearn import svm

class Training:
    def execute(self):
        try:
            docs_train, cls_train = self.__load_idn_dataset()
            idn_vectorizer, idn_classifier = self.__doTrain(docs_train, cls_train, VarGlobal.INDONESIA)
            self.__save(idn_vectorizer, VarGlobal.IDN_VECTORIZER_PATH)
            self.__save(idn_classifier, VarGlobal.IDN_CLASSIFIER_MODEL_PATH)

            docs_train, cls_train = self.__load_eng_dataset()
            eng_vectorizer, eng_classifier = self.__doTrain(docs_train, cls_train, VarGlobal.ENGLISH)
            self.__save(eng_vectorizer, VarGlobal.ENG_VECTORIZER_PATH)
            self.__save(eng_classifier, VarGlobal.ENG_CLASSIFIER_MODEL_PATH)
        except Exception as error: raise error

    def __doTrain(self, docs_train, cls_train, stopword_lang=""):
        """
        Fungsi ini digunakan untuk menjalankan proses training dan akan menghasilkan model training berupa model
        vektorisasi yang digunakan untuk preprocessing dan model classifier yang digunakna untuk klasifikasi
        :param docs_train: (list) daftar dokumen pelatihan
        :param cls_train: (list) daftar kategori dokumen pelatihan
        :param stopword_lang: (string) bahasa yang digunakan pada dokumen pelatihan
        :return: (object, object) nilai kembalian yang diberikan adalah 2 objek (model) vekrotisasi dan classifier
        """

        # set parameter binary=False jika menggunakan feature representation TF-IDF atau Int(frekuensi),
        # set parameter binary=True jika menggunakan feature representation binary
        vectorizer = Preprocess(ngram_range=(1,1),
                                binary=False,
                                stop_words=self.__get_stopword(lang=stopword_lang))

        # melakukan proses preprocessing
        docs_train_vector = vectorizer.fit_transform(docs_train)

        # melakukan proses learning dengan metode SVM Linear
        classifier = svm.LinearSVC()
        classifier.fit(docs_train_vector, cls_train)

        return vectorizer, classifier

    def __save(self, value, filename):
        """
        Fungsi ini digunakan untuk melakukan dumping objek python menjadi sebuah file
        :param value: (object) model atau objek yang akan di dumping
        :param filename: (string) path direktori hasil dumping
        :return:
        """
        joblib.dump(value, filename)

    def __load_eng_dataset(self):
        """
        Fungsi ini digunakan untuk load data training untuk bahasa inggris
        :return: (list) daftar data training bahasa inggris
        """
        return self.__load_dataset(VarGlobal.ENG_DOCS_TRAIN_PATH)

    def __load_idn_dataset(self):
        """
        Fungsi ini digunakan untuk load data training untuk bahasa indonesia
        :return: (list) daftar data training bahasa indonesia
        """
        return self.__load_dataset(VarGlobal.IDN_DOCS_TRAIN_PATH)

    def __load_dataset(self, doc_train_path = ""):
        """
        Fungsi ini digunakan untuk load data training
        :param doc_train_path: (string) path direktori daftar data training
        :return: (list) daftar data training
        """

        file = open(doc_train_path)
        lines = file.readlines()
        docs, cls, content, isContent = [], [], "", False
        for line in lines:
            if line.endswith('.sgm\n'):
                if(isContent):
                    docs.append(content)
                    isContent, content = False, ""
                if line.split(':')[1].strip() == VarGlobal.NEGATIVE_CLASS:
                    cls.append(VarGlobal.NEGATIVE_CLASS)
                else:
                    cls.append(VarGlobal.POSITIVE_CLASS)
            else:
                content += line
                isContent = True

        docs.append(content)
        return docs, cls

    def __get_stopword(self, lang = ""):
        """
        Fungsi ini digunakan untuk load data stopword dalam bahasa indonesia ataupun bahasa inggris
        :param lang: (string) bahasa stopword yang ingin di load
        :return: (list) daftar stopword
        """

        if lang == VarGlobal.INDONESIA:
            f = open(VarGlobal.IDN_STOPWORD_PATH)
            stopword = f.read().split()
            return frozenset(stopword)
        elif lang == VarGlobal.ENGLISH:
            f = open(VarGlobal.ENG_STOPWORD_PATH)
            stopword = f.read().split()
            return frozenset(stopword)
        else: return None