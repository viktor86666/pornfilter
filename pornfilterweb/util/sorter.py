__author__ = 'rama'
__date__ = '6/11/2015'

class Sorter(object):
    def sort(self, path):
        file = open(path, "r+")
        str_file = file.read()
        list = sorted(str_file.splitlines())
        file.truncate()
        file.close()
        file = open(path, "w+")
        file.write(self.print_list_to_file(list))
        file.close()

    def print_list_to_file(self, list):
        str = ""
        for s in list: str = str+s+"\n"
        return str

path_eng = "../res/porn-list-term/eng_porn_list_term.txt"
path_idn = "../res/porn-list-term/idn_porn_list_term.txt"
s = Sorter()
s.sort(path_idn)
