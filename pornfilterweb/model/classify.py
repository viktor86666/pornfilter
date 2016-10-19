__author__ = 'rama'
__date__ = '4/19/2015'

import langid
from model.global_app import VarGlobal
from sklearn.externals import joblib
from model.parser import Parser
from math import exp

class Classify:
    """
    Class ini merupakan kelas yang digunakan untuk melakukan klasifikasi
    """

    def __init__(self):
        self.__clf = None
        self.__vectorizer = None

    def __predict(self, text_content = ""):
        """
        Fungsi ini digunakan untuk melakukan prediksi atau klasifikasi berdasarkan teks konten webpage.
        :param text_content: (string) konten teks dari webpage
        :return: (list) hasil prediksi
        """

        language = self.detect_lang(text_content)
        print "Bahasa: ", language
        self.__clf = self.__load_classifier(language)
        self.__vectorizer = self.__load_vectorizer(language)
        document = [text_content]
        doc_vector = self.__vectorizer.transform(document)
        prediction = self.__clf.predict(doc_vector)
        decision = self.__clf.decision_function(doc_vector)
        coef = self.__clf.coef_[0]
        probability = 1. / (1 + exp((- (coef[0] / coef[1]))*decision[0]-(coef[3] / coef[1])))
        #print coef
        #print 'y = ' + str(- (coef[0] / coef[1])) + ' x + ' + str(-(coef[3] / coef[1]))
        # output berupa dictionary yang menyimpan "class" (prediksi kategori klasifikasi input),
        # dan "value" yang merupakan tingkat kepercayaan hasil prediksi (predict confidence scores)

        # contoh output jika di print
        # {'class': 'porno', 'confidence': -0.72431184642082558}

        return {"class": prediction[0], "probability": probability}

    def predictBasedURL(self, URL=""):
        """
        Fungsi ini digunakan untuk melakukan prediksi atau klasifikasi berdasarkan URL webpage.
        :param URL: (string) alamat URL dari situs
        :return: (list) hasil prediksi
        """

        # print "cheking url: %s \n... \n..." % URL
        # print "extracting data text ... ... \n... \n..."
        try:
            text_content = self.parser(URL)

            # import re
            # pattern = re.compile(r'\s+')
            # text_content = re.sub(pattern, ' ', text_content)
            # print "content : \n %s " % text_content
            # print "\n\n"

            return self.__predict(text_content)

        except Exception as error: raise error

    def predictBasedTextContent(self, text_content = ""):
        """
        Fungsi ini digunakan untuk melakukan prediksi atau klasifikasi berdasarkan teks konten webpage.
        :param text_content: (string) konten teks dari webpage
        :return: (list) hasil prediksi
        """

        try:
            return self.__predict(text_content)
        except Exception as error: raise error

    def parser(self, URL):
        """
        Fungsi ini digunakan untuk melakukan parsing konten teks dari file HTML. Dalam proses parsing dilakukan proses
        pembersihan tag-tag HTML dan script javascript atau css
        :param URL: (string) alamat URL dari situs.
        :return: (string) teks konten dari webpage
        """

        parser = Parser()
        parser.do_parse(URL)
        return parser.get_text_content()

    def detect_lang(self, text_content = ""):
        """
        Fungsi ini digunakan untuk melakukan deteksi bahasa dengan memamnfaatkan library langid.
        :param text_content: (string) konten teks dari web page.
        :return: (string) bahasa hasil deteksi
        """

        langid.set_languages(['en', 'id'])
        result = langid.classify(text_content)
        if(result[0] == "en"): return VarGlobal.ENGLISH
        else: return VarGlobal.INDONESIA

    def __load_classifier(self, languange):
        """
        Fungsi ini digunakan untuk melakukan load objek classifier yang telah dibuat pada saat proses training
        :param languange: (string) id bahasa yang digunakan. id "id" untuk bahasa indonesia dan id "en" untuk bahasa inggris
        :return: object classifier
        """

        if (languange == VarGlobal.ENGLISH):
            return self.__load_model(VarGlobal.ENG_CLASSIFIER_MODEL_PATH)
        else:
            return self.__load_model(VarGlobal.IDN_CLASSIFIER_MODEL_PATH)

    def __load_vectorizer(self, language):
        """
        Fungsi ini digunakan untuk melakukan load objek vectorizer yang telah dibuat pada saat proses training.
        :param language: (string) id bahasa yang digunakan. id "id" untuk bahasa indonesia dan id "en" untuk bahasa inggris
        :return: (object) vectorizer
        """

        if (language == VarGlobal.ENGLISH):
            return self.__load_model(VarGlobal.ENG_VECTORIZER_PATH)
        else:
            return self.__load_model(VarGlobal.IDN_VECTORIZER_PATH)

    def __load_model(self, filename):
        """
        Fungsi ini digunakan untuk malakukan load objek hasil dump dari proses training
        :param filename: (string) path direktori letak file penyimpanan objek hasil dumping
        :return: (object)
        """

        return joblib.load(filename)