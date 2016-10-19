from django.utils.encoding import smart_str, smart_unicode
from ast import literal_eval
import ast
import string
import random
import time
import sys
import datetime
import requests
import math
import urlparse
import os.path
import os
import subprocess
import urllib2,urllib,cookielib
import re
from urllib import urlretrieve
from urlparse import urlparse
from time import gmtime, strftime
from bs4 import BeautifulSoup
import imghdr
from PIL import Image
reload(sys)
sys.setdefaultencoding("utf-8")
jumlahteksporno = []
jumlahgambar = []
linkgambar = []
jumlahgambarporno = []
jumlahgambartidakporno = []
linkgambarporno = []
linksudahada = []
jumlahteksporno = []
listteksporno = []
print "Deteksi Teks"
pt = 0
url = sys.argv[1]
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
	page = opener.open(req)
except opener.HTTPError, e:
	print e.fp.read()
	page = urllib.urlopen(url)
content = page.read()
parsed = urlparse(url).netloc
urlpath = urlparse(url).path
urlpath = urlpath.replace("/",".")
parsed = parsed.replace('www.','')
parsed = parsed + str(urlpath)
out_folder = "/home/yosuaalvin/porndetection/text/"+parsed
out_situs = "/var/www/html/"+parsed
if not os.path.exists(out_folder):
	try:
		subprocess.check_output("mkdir "+out_folder, shell=True)
	except subprocess.CalledProcessError:
		pass
if not os.path.exists(out_situs):
	try:
		subprocess.check_output("mkdir "+out_situs, shell=True)
	except subprocess.CalledProcessError:
		pass
out_folder_g = "/home/yosuaalvin/porndetection/gambar/"+parsed
out_gambar = "/var/www/html/"+parsed+"/gambar"
out_situs = "/var/www/html/"+parsed
if not os.path.exists(out_folder_g):
	try:
		subprocess.check_output("mkdir "+out_folder_g, shell=True)
	except subprocess.CalledProcessError:
		pass
if not os.path.exists(out_situs):
	try:
		subprocess.check_output("mkdir "+out_situs, shell=True)
	except subprocess.CalledProcessError:
		pass
if not os.path.exists(out_gambar):
	try:
		subprocess.check_output("mkdir "+out_gambar, shell=True)
	except subprocess.CalledProcessError:
		pass
soup = BeautifulSoup(content)
for script in soup(["script", "style"]):
	script.extract()    # rip it out
text = soup.get_text()
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
textreplace = textreplace.replace(", ","\\n")
print "Halaman Website:\n" + str(textreplace)
listtext = literal_eval(textlatest)
try:
	teksporno = subprocess.check_output("python text_filtering.py -c -u "+url,shell=True)
	teksporno = ast.literal_eval(teksporno)
	#print "Probability:" + str(teksporno['probability'])
	pt = str(teksporno['probability'])
	if (teksporno['class']=='porno'):
		print "Teks Porno"
		with open('/home/yosuaalvin/porndetection/eng_porn_list_term.txt','r') as f:
			for line in f:
				for word in line.split():
					if word in smart_str(text.split()):
						listteksporno.append(word)
						jumlahteksporno.append(1)
						content = content.replace(word,"******")
		with open('/home/yosuaalvin/porndetection/idn_porn_list_term.txt','r') as f2:
			for line2 in f2:
				for word2 in line2.split():
					if word2 in smart_str(text.split()):
						listteksporno.append(word2)
						jumlahteksporno.append(1)
						content = content.replace(word2,"******")
	else:
		print "Teks Tidak Porno"
	hasiltapisteks = open("/home/yosuaalvin/porndetection/text/"+parsed+"/hasil.html","w+")
	print >> hasiltapisteks, content
	hasilsitus = open("/var/www/html/"+parsed+"/hasil.html","w+")
	print >> hasilsitus, content
except subprocess.CalledProcessError:
	pass
print "Kata porno:\n" + str(listteksporno)
print "Jumlah seluruh teks: " + str(len(listtext))
print "Jumlah teks porno: " + str(sum(jumlahteksporno))
#print "http://localhost/download/"+parsed+"/hasil.html"
#Gambar
req = urllib2.Request(url, headers=hdr)
cookiejar = cookielib.LWPCookieJar()
opener = urllib2.build_opener( urllib2.HTTPCookieProcessor(cookiejar) )
try:
	page = opener.open(req)
except opener.HTTPError, e:
	print e.fp.read()
	page = urllib.urlopen(url)
content = page.read()
soup = BeautifulSoup(content)
print "------------------"
print "Deteksi Gambar"
jmlgambar = len(soup.findAll('img'))
#print jmlgambar
simpangambar = open("/home/yosuaalvin/porndetection/gambar/"+parsed+"/gambar.txt","w+")
print >> simpangambar, ""
for i in range(0,jmlgambar):
	gambars = ""
	try:
		gambars = soup.findAll('img')[i]['src']
	except:
		pass
		try:
			gambars = soup.findAll('img')[i]['data-interchange']
			gambars = gambars.replace("[","")
			gambars = gambars.split(',', 1)[0]
		except:
			pass
	if gambars.strip().startswith('//'):
		gambars = gambars.replace('//','http://')
		simpangambar = open("/home/yosuaalvin/porndetection/gambar/"+parsed+"/gambar.txt","a+")
		print >> simpangambar, gambars
		print gambars
		jumlahgambar.append(1)
		linkgambar.append(gambars)
		filename = gambars.split("/")[-1]
		filename = filename.split("?")[0]
		outpath = os.path.join(out_gambar, filename)
		if (os.path.exists(outpath)):
			print "File sudah ada"
			linksudahada.append(1)
			pass
		else:
			try:
				urlretrieve(gambars, outpath)
				try:
					test = Image.open(outpath).verify()
					tipe = imghdr.what(outpath)
					if (tipe=='gif'):
						frame = Image.open(outpath)
						frame.save( '%s' % (outpath), 'GIF')
						pass
						inFile = Image.open(outpath).convert('RGB') 
						fileName = os.path.splitext(outpath)[0]
						outFile = fileName + ".jpg" 
						inFile.save(outFile)
						#Image.open(outpath).convert('RGB').save(os.path.splitext(outpath)[0]+".jpg")
					if (tipe=='png'):
						inFile = Image.open(outpath).convert('RGB') 
						fileName = os.path.splitext(outpath)[0]
						outFile = fileName + ".jpg" 
						inFile.save(outFile)
					(width,height) = Image.open(os.path.splitext(outpath)[0]+".jpg").size
					if (width==height):
						hapusthumbnail = subprocess.check_output("rm -rf "+os.path.splitext(outpath)[0]+".jpg",shell=True)
						hapusthumbnailasli = subprocess.check_output("rm -rf "+outpath,shell=True)
					else:
						try:
							gambarporno = subprocess.check_output("python pija.py "+os.path.splitext(outpath)[0]+".jpg",shell=True)
							if (str(1) in gambarporno):
								print "Gambar Porno"
								jumlahgambarporno.append(1)
								linkgambarporno.append(gambars)
							elif (str(0) in gambarporno or str("cow") or str("wood") or str("sand") in outpath):
								print "Gambar Tidak Porno"
								jumlahgambartidakporno.append(1)
						except subprocess.CalledProcessError:
							print "Gambar Tidak Terdeteksi"
							pass
				except:
					pass
			except:
				pass
	else:
		jumlahgambar.append(1)
		linkgambar.append(gambars)
		filename = gambars.split("/")[-1]
		filename = filename.split("?")[0]
		outpath = os.path.join(out_gambar, filename)
		if (os.path.exists(outpath)):
			print "File sudah ada"
			linksudahada.append(1)
			pass
		else:
			simpangambar = open("/home/yosuaalvin/porndetection/gambar/"+parsed+"/gambar.txt","a+")
			print >> simpangambar, gambars
			print gambars
			filename = gambars.split("/")[-1]
			filename = filename.split("?")[0]
			outpath = os.path.join(out_gambar, filename)
			try:
				urlretrieve(gambars, outpath)
				try:
					test = Image.open(outpath).verify()
					tipe = imghdr.what(outpath)
					if (tipe=='gif'):
						frame = Image.open(outpath)
						frame.save( '%s' % (outpath), 'GIF')
						pass
						inFile = Image.open(outpath).convert('RGB')
						fileName = os.path.splitext(outpath)[0]
						outFile = fileName + ".jpg" 
						inFile.save(outFile)
						#Image.open(outpath).convert('RGB').save(os.path.splitext(outpath)[0]+".jpg")
					if (tipe=='png'):
						inFile = Image.open(outpath).convert('RGB') 
						fileName = os.path.splitext(outpath)[0]
						outFile = fileName + ".jpg" 
						inFile.save(outFile)
					(width,height) = Image.open(os.path.splitext(outpath)[0]+".jpg").size
					if (width==height):
						hapusthumbnail = subprocess.check_output("rm -rf "+os.path.splitext(outpath)[0]+".jpg",shell=True)
						hapusthumbnailasli = subprocess.check_output("rm -rf "+outpath,shell=True)
					else:
						try:
							gambarporno = subprocess.check_output("python pija.py "+os.path.splitext(outpath)[0]+".jpg",shell=True)
							if (str(1) in gambarporno):
								print "Gambar Porno"
								jumlahgambarporno.append(1)
								linkgambarporno.append(gambars)
							elif (str(0) in gambarporno or str("cow") or str("wood") or str("sand") in outpath):
								print "Gambar Tidak Porno"
								jumlahgambartidakporno.append(1)
						except subprocess.CalledProcessError:
							print "Gambar Tidak Terdeteksi"
							pass
				except:
					pass
			except:
				pass
#print "Jumlah gambar dalam script"
jmlgambarscript = sum(1 for o in re.finditer("(url\(.*(?:.jpg|.gif|.png|.bmp|.tiff)\))",str(soup)))
#print sum(1 for o in re.finditer("(url\(.*(?:.jpg|.gif|.png|.bmp|.tiff)\))",str(soup)))
gmbr = str(re.findall("(url\(.*(?:.jpg|.gif|.png|.bmp|.tiff)\))",str(soup)))
gmbr = gmbr.replace("[","")
gmbr = gmbr.replace("\'url(","")
gmbr = gmbr.replace(")\',",",")
gmbr = gmbr.replace(")\']","")
gmbrs = gmbr.split(",")
for gs in gmbrs:
	simpangmbr = open("/home/yosuaalvin/porndetection/gambar/"+parsed+"/gambar.txt","a+")
	if len(gs) > 2:
		print gs
		print >> simpangmbr, gs
		jumlahgambar.append(1)
		linkgambar.append(gs)
		filename = gs.split("/")[-1]
		filename = filename.split("?")[0]
		outpath = os.path.join(out_gambar, filename)
		if (os.path.exists(outpath)):
			print "File sudah ada"
			linksudahada.append(1)
			pass
		else:
			try:
				urlretrieve(gs, outpath)
				try:
					test = Image.open(outpath).verify()
					tipe = imghdr.what(outpath)
					if (tipe=='gif'):
						frame = Image.open(outpath)
						frame.save( '%s' % (outpath), 'GIF')
						pass
						inFile = Image.open(outpath).convert('RGB') 
						fileName = os.path.splitext(outpath)[0]
						outFile = fileName + ".jpg" 
						inFile.save(outFile)
						#Image.open(outpath).convert('RGB').save(os.path.splitext(outpath)[0]+".jpg")
					if (tipe=='png'):
						inFile = Image.open(outpath).convert('RGB') 
						fileName = os.path.splitext(outpath)[0]
						outFile = fileName + ".jpg" 
						inFile.save(outFile)
					(width,height) = Image.open(os.path.splitext(outpath)[0]+".jpg").size
					if (width==height):
						hapusthumbnail = subprocess.check_output("rm -rf "+os.path.splitext(outpath)[0]+".jpg",shell=True)
						hapusthumbnailasli = subprocess.check_output("rm -rf "+outpath,shell=True)
					else:
						try:
							gambarporno = subprocess.check_output("python pija.py "+os.path.splitext(outpath)[0]+".jpg",shell=True)
							if (str(1) in gambarporno):
								print "Gambar Porno"
								jumlahgambarporno.append(1)
								linkgambarporno.append(gambars)
							elif (str(0) in gambarporno or str("cow") or str("wood") or str("sand") in outpath):
								print "Gambar Tidak Porno"
								jumlahgambartidakporno.append(1)
						except subprocess.CalledProcessError:
							print "Gambar Tidak Terdeteksi"
							pass
				except:
					pass
			except:
				pass
print "Jumlah gambar porno: " + str(sum(jumlahgambarporno))
print "Jumlah gambar tidak porno: " + str(sum(jumlahgambartidakporno))
p1 = 0.31
p2 = 0.29
n1 = float(sum(jumlahgambarporno))
n2 = float(sum(jumlahgambartidakporno))
print "pt: " + str(pt)
print "p1: " + str(p1)
print "p2: " + str(p2)
print "n1: " + str(n1)
print "n2: " + str(n2)
a = (1 - p2)
a = a**n1
b = p2 ** n2
c = float(pt)
g = a * b * c
d = p1 ** n1
e = (1 - p1)
e = e**n2
f = (1 - float(pt))
h = d * e * f 
factor = float(g / h)
print "Decision Factor: " + str(factor)
if (factor>=1):
	print "Situs Porno"
	for gp in linkgambar:
		content = content.replace(gp,"http://202.169.224.53/stop.jpg")
		hasiltapisgambar = open("/home/yosuaalvin/porndetection/gambar/"+parsed+"/hasilgambar.html","w+")
		print >> hasiltapisgambar, content
		hasilsitus = open("/var/www/html/"+parsed+"/hasilgambar.html","w+")
		print >> hasilsitus, content
else:
	print "Situs Tidak Porno"