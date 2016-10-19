__author__ = 'rama'
__date__ = '6/5/2015'

from optparse import OptionParser
from model.training import Training
from model.classify import Classify
from model.global_app import VarGlobal


def main():
    op = OptionParser()
    op.add_option("-t", "--training",
                  action = "store_true", default=False, dest="do_training",
                  help="Melakukan proses training dan menghasilkan model pengklasifikasi"
                  )
    op.add_option("-c", "--classify", action="store_true", default=False, dest="do_classify",
                  help="Melakukan proses klasifikasi terhadap input URL atau teks dokumen yang diberikan"
                  )
    op.add_option("-u", "--url", type="string", dest="input_url",
                  help="Untuk memberikan inputan URL"
                  )
    op.add_option("-d", "--text", type="string", dest="input_text",
                  help="Untuk memberikan inputan teks dokumen"
                  )
    (opts, args) = op.parse_args()

    if opts.do_training:
        Training().execute()

    elif opts.do_classify:
        try:
            # instansiasi objek Classify yang digunakan untuk melakukan klasifikasi teks
            classifier = Classify()

            # mengecek option inputan yang diberikan. apakah akan dilakukan prediksi berdasarkan URL atau teks konten
            if opts.input_url:
                output = classifier.predictBasedURL(opts.input_url)
            elif opts.input_text:
                output = classifier.predictBasedTextContent(opts.input_text)

            print output

            # output berupa dictionary yang menyimpan "class" (prediksi kategori klasifikasi input),
            # dan "confidence" yang merupakan tingkat kepercayaan hasil prediksi (predict confidence scores)
            # contoh output jika di print
            # {'class': 'porno', 'confidence': -0.72431184642082558}
        except Exception as error:
            print(error)


if __name__ == "__main__": main()