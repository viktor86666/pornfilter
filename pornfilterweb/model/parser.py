__author__ = 'rama'
__date__ = '3/19/2015'

from bs4 import BeautifulSoup
from urlparse import urlparse
import urllib2
from django.utils.encoding import smart_str, smart_unicode
import string
import sys
import cookielib
reload(sys)
sys.setdefaultencoding("utf-8")
class Parser:
    def __init__(self):
        self.__html_doc = "";
        self.__content_text = "";
        self.__domain_name = "";
        self.__links = [];

    def do_parse(self, url = ""):
        """
        Fungsi ini digunakan untuk melakukan eksekusi proses parsing konten teks pada HTML
        :param url: (string)
        :return:
        """
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        req = urllib2.Request(url, headers=hdr)
        cookiejar = cookielib.LWPCookieJar()
        opener = urllib2.build_opener( urllib2.HTTPCookieProcessor(cookiejar) )
        try:
            html_doc = opener.open(req)
        except opener.HTTPError, e:
            print e.fp.read()
            html_doc = urllib.urlopen(url)
        self.__html_doc = html_doc;
        self.__domain_name = self.__parse_domain(url);
        self.__parser_text();

    def __parser_text(self):
        """
        Fungsi inin digunakan untuk parsing text html/menghapus tag html
        :return:
        """
        #=========== Menggunakan BS4 =================
        soup = BeautifulSoup(self.__html_doc);

        # hapus tag <script> dan kontennya
        [s.extract() for s in soup('script')]

        # hapus tag <style> dan kontennya
        [s.extract() for s in soup('style')]

        # cara lain hapus tag <script>
        # [x.extract() for x in soup.findAll('script')]

        #=========== Menggunakan NLTK =================
        # text = nltk.clean_html(html_doc);

        text = soup.get_text().lower();
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        textwounicode = text.decode('unicode_escape').encode('ascii','ignore')
        exclude = set(string.punctuation)
        table = string.maketrans("","")
        textwopunctuation = textwounicode.translate(table, string.punctuation)
        textwonumber = ''.join([i for i in textwopunctuation if not i.isdigit()])
        textlatest = smart_str(textwonumber.split())
        textreplace = textlatest.replace("[","")
        textreplace = textreplace.replace("]","")
        textreplace = textreplace.replace("'","")
        textreplace = textreplace.replace(", ","\n")
        self.__content_text = textreplace
        # ambil semua link yg ada pada webpage
        # links = [];
        # for a in soup.find_all('a'):
        #     link = a.get('href');
        #     if str(link).startswith('http'): links.append(link);
        #     #links.append(link);
        # self.__links = links;

    def __parse_domain(self, url = ""):
        parsed_uri = urlparse(url);
        return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri);

    def get_text_content(self):
        """
        Fungsi ini mermberikan return konten teks hasil parsing
        :return: (string) konten teks hasil parsing
        """
        return self.__content_text;

    def get_domain_name(self):
        """
        Fungsi ini memberikan return domain name hasil parsing
        :return: (string) domain name
        """
        return self.__domain_name;

    def get_links(self):
        """
        Fungsi ini memberikan return daftar back link yang ada dalam webpage
        :return: (list) daftar link
        """
        return self.__links;
