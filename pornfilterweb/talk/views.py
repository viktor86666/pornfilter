from __future__ import division
from django.shortcuts import render
from django.http import HttpResponse
from talk.models import Post
from talk.forms import PostForm
from model.training import Training
from model.classify import Classify
from model.global_app import VarGlobal
from django.utils.encoding import smart_str, smart_unicode
from ast import literal_eval
from pymongo import MongoClient
from urlparse import urlparse
import urllib2,urllib,cookielib
from urllib import urlretrieve
from urlparse import urlparse
from time import gmtime, strftime
from bs4 import BeautifulSoup
import imghdr
from PIL import Image
import subprocess
import json
import os
import sys
import string
import re
import mechanize
import cookielib
client = MongoClient()
db = client.ugm
coll = db.antrian
collbaru = db.antrianbaru
reload(sys)
sys.setdefaultencoding("utf-8")
def home(req):

    tmpl_vars = {
        'all_posts': Post.objects.reverse(),
        'form': PostForm()
    }
    return render(req, 'talk/index.html', tmpl_vars)

def browsing(request):
        return HttpResponse("testing")

def text_process(request):
    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        #print post_text
        jumlahteksporno = []
        listteksporno = []
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
        req = urllib2.Request(post_text, headers=hdr)
        try:
            page = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e.fp.read()
        page = urllib.urlopen(post_text)
        br = mechanize.Browser()
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)
        br.set_handle_equiv(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        r = br.open(post_text)        
        content = page.read()
        #print content
        if "denied" in content:
        	content = r.read()
        print content
        parsed = urlparse(post_text).netloc
        urlpath = urlparse(post_text).path
        urlpath = urlpath.replace("/",".")
        parsed = parsed.replace('www.','')
        parsed = parsed + str(urlpath)
        out_situs = "/usr/share/nginx/html/download/"+parsed
        if not os.path.exists(out_situs):
            os.mkdir(out_situs)
        soup = BeautifulSoup(content)
        for script in soup(["script", "style"]):
            script.extract()
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
        listtext = literal_eval(textlatest)
        print listtext
        #Training().execute()
        try:
            classifier = Classify()
            output = classifier.predictBasedURL(post_text)
            hasil = output.get("class")
            #print output
            if (hasil=="porno"):
                replacedText = ""
                textlist = []
                with open('talk/pornoList_Eng.txt','r') as f:
                    for line in f:
                        line = line.decode('unicode_escape').encode('ascii','ignore')
                        line = line.rstrip('\r\n')
                        textlist.append(line)
                        for word in line.split():
                            if word in smart_str(text.split()):
                                listteksporno.append(word)
                                jumlahteksporno.append(1)
                print textlist
                pattern = "r'(?i)|"+'|'.join(textlist)
                textPattern = re.compile(pattern)
                for t in soup.findAll(text=textPattern):
                    t.replaceWith(re.sub(textPattern, "****", t))
                    replacedText = basestring.__str__(soup)
                with open('talk/pornoList_Ind.txt','r') as f:
                    for line in f:
                        line = line.decode('unicode_escape').encode('ascii','ignore')
                        line = line.rstrip('\r\n')
                        textlist.append(line)
                        for word2 in line.split():
                            if word2 in smart_str(text.split()):
                                listteksporno.append(word2)
                                jumlahteksporno.append(1)
                pattern = "r'(?i)|"+'|'.join(textlist)
                textPattern = re.compile(pattern)
                for t in soup.findAll(text=textPattern):
                    t.replaceWith(re.sub(textPattern, "****", t))
                    replacedText = basestring.__str__(soup)
                print replacedText
                hasilsitus = open("/usr/share/nginx/html/download/"+parsed+"/hasilteks.html","w+")
                print >> hasilsitus, replacedText
                jumlahteks = (str(len(listtext)))
                jumlahteksporno = (str(sum(jumlahteksporno)))
                response_data = {}
                response_data['jumlahteks'] = jumlahteks
                response_data['jumlahteksporno'] = jumlahteksporno
                response_data['keputusan'] = "This site is contain negative text"
                response_data['hasil'] = "http://202.169.224.53/download/"+parsed+"/hasilteks.html"
                return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json"
                )
            elif (hasil=="tidak-porno"):
                textlist = []
                with open('talk/pornoList_Eng.txt','r') as f:
                    for line in f:
                        line = line.decode('unicode_escape').encode('ascii','ignore')
                        line = line.rstrip('\r\n')
                        textlist.append(line)
                        for word in line.split():
                            if word in smart_str(text.split()):
                                listteksporno.append(word)
                                jumlahteksporno.append(1)
                print textlist
                pattern = "r'(?i)|"+'|'.join(textlist)
                textPattern = re.compile(pattern)
                for t in soup.findAll(text=textPattern):
                    t.replaceWith(re.sub(textPattern, "****", t))
                    replacedText = basestring.__str__(soup)
                with open('talk/pornoList_Ind.txt','r') as f:
                    for line in f:
                        line = line.decode('unicode_escape').encode('ascii','ignore')
                        line = line.rstrip('\r\n')
                        textlist.append(line)
                        for word2 in line.split():
                            if word2 in smart_str(text.split()):
                                listteksporno.append(word2)
                                jumlahteksporno.append(1)
				pattern = "r'(?i)|"+'|'.join(textlist)
                textPattern = re.compile(pattern)
                for t in soup.findAll(text=textPattern):
                    t.replaceWith(re.sub(textPattern, "****", t))
                    replacedText = basestring.__str__(soup)
                jumlahteks = (str(len(listtext)))
                jumlahteksporno = (str(sum(jumlahteksporno)))
                persenteks = int(jumlahteksporno)/int(jumlahteks)
                if (persenteks>0.2):
                    hasilsitus = open("/usr/share/nginx/html/download/"+parsed+"/hasilteks.html","w+")
                    print >> hasilsitus, replacedText
                    response_data = {}
                    response_data['jumlahteks'] = jumlahteks
                    response_data['jumlahteksporno'] = jumlahteksporno
                    response_data['keputusan'] = "This site contain negative text"
                    response_data['hasil'] = "http://202.169.224.53/download/"+parsed+"/hasilteks.html"
                else:
                    response_data = {}
                    response_data['jumlahteks'] = jumlahteks
                    response_data['jumlahteksporno'] = jumlahteksporno
                    response_data['keputusan'] = "This site doesn't contain negative text"
                    response_data['hasil'] = post_text				
                return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json"
                )
        except Exception as error:
            print(error)


def image_process(request):
    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        x = collbaru.find({"url":post_text,"status":"porn"}).count()
        y = collbaru.find({"url":post_text,"status":"porn"})
        if (x>0):
			parsed = urlparse(post_text).netloc
			urlpath = urlparse(post_text).path
			urlpath = urlpath.replace("/",".")
			parsed = parsed.replace('www.','')
			parsed = parsed + str(urlpath)
			response_data = {}
			response_data['jumlahgambar'] = y[0]['n1'] + y[0]['n2']
			response_data['jumlahgambarporno'] = y[0]['n1']
			response_data['decisionfactor'] = y[0]['factor']
			response_data['keputusan'] = "This site is contain negative image"
			response_data['hasil'] = "http://202.169.224.53/download/"+parsed+"/hasilgambar.html"
			return HttpResponse(
				json.dumps(response_data),
				content_type="application/json"
			)
        else:
			checkimage = 'python ' + os.path.dirname(os.path.realpath(__file__))+'/pija.py '
			#print checkimage
			checkimageporn = os.path.dirname(os.path.realpath(__file__))+'/./porntest '
			#print checkimageporn
			linkgambar = []
			jumlahgambarporno = []
			jumlahgambartidakporno = []
			pt = 0
			hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			'Accept-Encoding': 'none',
			'Accept-Language': 'en-US,en;q=0.8',
			'Connection': 'keep-alive'}
			req = urllib2.Request(post_text, headers=hdr)
			cookiejar = cookielib.LWPCookieJar()
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
			try:
				page = urllib2.urlopen(req)
			except urllib2.HTTPError, e:
				print e.fp.read()
			page = urllib.urlopen(post_text)
			br = mechanize.Browser()
			cj = cookielib.LWPCookieJar()
			br.set_cookiejar(cj)
			br.set_handle_equiv(True)
			br.set_handle_redirect(True)
			br.set_handle_referer(True)
			br.set_handle_robots(False)
			br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
			br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
			r = br.open(post_text)        
			content = page.read()
			#print content
			if "denied" in content:
				content = r.read()
			soup = BeautifulSoup(content)
			parsed = urlparse(post_text).netloc
			urlpath = urlparse(post_text).path
			urlpath = urlpath.replace("/",".")
			parsed = parsed.replace('www.','')
			parsed = parsed + str(urlpath)
			out_situs = "/usr/share/nginx/html/download/"+parsed
			out_gambar = "/usr/share/nginx/html/download/"+parsed+"/gambar"
			if not os.path.exists(out_situs):
				os.mkdir(out_situs)
			if not os.path.exists(out_gambar):
				os.mkdir(out_gambar)
			soup = BeautifulSoup(content)
			for script in soup(["script", "style"]):
				script.extract()
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
			listtext = literal_eval(textlatest)
			#print listtext
			#Training().execute()
			try:
				classifier = Classify()
				output = classifier.predictBasedURL(post_text)
				hasil = output.get("probability")
				pt = hasil
			except Exception as error:
				print(error)
			req = urllib2.Request(post_text, headers=hdr)
			cookiejar = cookielib.LWPCookieJar()
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
			try:
				page = urllib2.urlopen(req)
			except urllib2.HTTPError, e:
				print e.fp.read()
			page = urllib.urlopen(post_text)
			content = page.read()
			soup = BeautifulSoup(content)
			jmlgambar = len(soup.findAll('img'))
			print jmlgambar
			simpangambar = open("/usr/share/nginx/html/download/"+parsed+"/gambar.txt","w+")
			print >> simpangambar, ""
			for i in range(0,jmlgambar):
				gambars = ""
				try:
					gambars = soup.findAll('img')[i]['src']
					#print gambars
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
					simpangambar = open("/usr/share/nginx/html/download/"+parsed+"/gambar.txt","a+")
					print >> simpangambar, gambars
					print gambars
					linkgambar.append(gambars)
					filename = gambars.split("/")[-1]
					filename = filename.split("?")[0]
					outpath = os.path.join(out_gambar, filename)
					if (os.path.exists(outpath)):
						print "File sudah ada"
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
										gambarporno = ""
										if (float(pt)<0.45):
											gambarporno = subprocess.check_output(checkimage+os.path.splitext(outpath)[0]+".jpg",shell=True)
										elif (float(pt)>0.45):
											gambarporno = subprocess.check_output(checkimageporn+os.path.splitext(outpath)[0]+".jpg",shell=True)
										#gambarporno = subprocess.check_output(checkimage+os.path.splitext(outpath)[0]+".jpg",shell=True)
										if (str(1) in gambarporno):
											print "Gambar Porno"
											jumlahgambarporno.append(1)
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
					linkgambar.append(gambars)
					filename = gambars.split("/")[-1]
					filename = filename.split("?")[0]
					outpath = os.path.join(out_gambar, filename)
					if (os.path.exists(outpath)):
						print "File sudah ada"
						pass
					else:
						simpangambar = open("/usr/share/nginx/html/download/"+parsed+"/gambar.txt","a+")
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
										gambarporno = ""
										if (float(pt)<0.45):
											gambarporno = subprocess.check_output(checkimage+os.path.splitext(outpath)[0]+".jpg",shell=True)
										elif (float(pt)>0.45):
											gambarporno = subprocess.check_output(checkimageporn+os.path.splitext(outpath)[0]+".jpg",shell=True)
										#gambarporno = subprocess.check_output(checkimage+os.path.splitext(outpath)[0]+".jpg",shell=True)
										if (str(1) in gambarporno):
											print "Gambar Porno"
											jumlahgambarporno.append(1)
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
			totalgambar = n1 + n2 
			factor = float(g / h)
			n = n1+n2
			fbaru = 0
			print "Decision Factor: " + str(factor)
			fpembilang = ((((1 + p1 - p2)**n1) * ((1 + p2 - p1)**n2)) - ((p1 ** n1)*((1 - p1)**n2) * (((1-p1)+p2)**n))) * float(pt)
			#print fpembilang
			fpenyebut = ((2**n)-((1-p1+p2)**n)) * (p1**n1*((1-p1)**n2)) * (1-float(pt))
			#print fpenyebut
			if (fpenyebut>0):
				fbaru = float(fpembilang/fpenyebut)
			elif(fpenyebut==0):
				fbaru = factor
			#print fbaru
			print "Decision Factor Modified: " + str(fbaru)
			if (fbaru>=1):
				print "Situs Porno"
				for gp in linkgambar:
					content = content.replace(gp,"http://202.169.224.53/stop.jpg")
					hasilsitus = open("/usr/share/nginx/html/download/"+parsed+"/hasilgambar.html","w+")
					print >> hasilsitus, content
				response_data = {}
				response_data['jumlahgambar'] = totalgambar
				response_data['jumlahgambarporno'] = n1
				response_data['decisionfactor'] = factor
				response_data['keputusan'] = "This site is contain negative image"
				response_data['hasil'] = "http://202.169.224.53/download/"+parsed+"/hasilgambar.html"
				return HttpResponse(
					json.dumps(response_data),
					content_type="application/json"
				)
			else:
				print "Situs Tidak Porno"
				response_data = {}
				response_data['jumlahgambar'] = totalgambar
				response_data['jumlahgambarporno'] = n1
				response_data['decisionfactor'] = factor
				response_data['keputusan'] = "This site doesn't contain negative image"
				response_data['hasil'] = post_text
				return HttpResponse(
					json.dumps(response_data),
					content_type="application/json"
				)
def text_image_process(request):
    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        x = collbaru.find({"url":post_text,"status":"porn"}).count()
        y = collbaru.find({"url":post_text,"status":"porn"})
        if (x>0):
			parsed = urlparse(post_text).netloc
			urlpath = urlparse(post_text).path
			urlpath = urlpath.replace("/",".")
			parsed = parsed.replace('www.','')
			parsed = parsed + str(urlpath)
			response_data = {}
			response_data['jumlahgambar'] = y[0]['n1'] + y[0]['n2']
			response_data['jumlahgambarporno'] = y[0]['n1']
			response_data['decisionfactor'] = y[0]['factor']
			response_data['keputusan'] = "This site is contain negative image"
			response_data['hasil'] = "http://202.169.224.53/download/"+parsed+"/hasilgambar.html"
			return HttpResponse(
				json.dumps(response_data),
				content_type="application/json"
			)
        else:
			parsed_uri = urlparse(post_text)
			domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
			checkimage = 'python ' + os.path.dirname(os.path.realpath(__file__))+'/pija.py '
			#print checkimage
			checkimageporn = os.path.dirname(os.path.realpath(__file__))+'/./porntest '
			#print checkimageporn
			jumlahteksporno = []
			listteksporno = []
			linkgambar = []
			jumlahgambarporno = []
			jumlahgambartidakporno = []
			persenteks = 0
			pt = 0
			hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			'Accept-Encoding': 'none',
			'Accept-Language': 'en-US,en;q=0.8',
			'Connection': 'keep-alive'}
			req = urllib2.Request(post_text, headers=hdr)
			cookiejar = cookielib.LWPCookieJar()
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
			try:
				page = urllib2.urlopen(req)
			except urllib2.HTTPError, e:
				print e.fp.read()
			page = urllib.urlopen(post_text)
			br = mechanize.Browser()
			cj = cookielib.LWPCookieJar()
			br.set_cookiejar(cj)
			br.set_handle_equiv(True)
			br.set_handle_redirect(True)
			br.set_handle_referer(True)
			br.set_handle_robots(False)
			br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
			br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
			r = br.open(post_text)        
			content = page.read()
			#print content
			if "denied" in content:
				content = r.read()
			soup = BeautifulSoup(content)
			parsed = urlparse(post_text).netloc
			urlpath = urlparse(post_text).path
			urlpath = urlpath.replace("/",".")
			parsed = parsed.replace('www.','')
			parsed = parsed + str(urlpath)
			out_situs = "/usr/share/nginx/html/download/"+parsed
			out_gambar = "/usr/share/nginx/html/download/"+parsed+"/gambar"
			if not os.path.exists(out_situs):
				os.mkdir(out_situs)
			if not os.path.exists(out_gambar):
				os.mkdir(out_gambar)
			soup = BeautifulSoup(content)
			for script in soup(["script", "style"]):
				script.extract()
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
			listtext = literal_eval(textlatest)
			print listtext
			#Training().execute()
			try:
				classifier = Classify()
				output = classifier.predictBasedURL(post_text)
				hasil = output.get("probability")
				pt = hasil
				kelas = output.get("class")
				print kelas
				if (kelas=="porno"):
					textlist = []
					with open('talk/pornoList_Eng.txt','r') as f:
						for line in f:
							line = line.decode('unicode_escape').encode('ascii','ignore')
							line = line.rstrip('\r\n')
							textlist.append(line)
							for word in line.split():
								if word in smart_str(text.split()):
									listteksporno.append(word)
									jumlahteksporno.append(1)
					with open('talk/pornoList_Ind.txt','r') as f:
						for line in f:
							line = line.decode('unicode_escape').encode('ascii','ignore')
							line = line.rstrip('\r\n')
							textlist.append(line)
							for word2 in line.split():
								if word2 in smart_str(text.split()):
									listteksporno.append(word2)
									jumlahteksporno.append(1)
					jumlahteks = len(listtext)
					print jumlahteks
					jumlahteksporno = sum(jumlahteksporno)
					print jumlahteksporno				
					persenteks = jumlahteksporno/jumlahteks
					print persenteks
				elif (kelas=="tidak-porno"):
					textlist = []
					with open('talk/pornoList_Eng.txt','r') as f:
						for line in f:
							line = line.decode('unicode_escape').encode('ascii','ignore')
							line = line.rstrip('\r\n')
							textlist.append(line)
							for word in line.split():
								if word in smart_str(text.split()):
									listteksporno.append(word)
									jumlahteksporno.append(1)
					with open('talk/pornoList_Ind.txt','r') as f:
						for line in f:
							line = line.decode('unicode_escape').encode('ascii','ignore')
							line = line.rstrip('\r\n')
							textlist.append(line)
							for word2 in line.split():
								if word2 in smart_str(text.split()):
									listteksporno.append(word2)
									jumlahteksporno.append(1)
					jumlahteks = len(listtext)
					jumlahteksporno = sum(jumlahteksporno)
					if (jumlahteks==0):
						persenteks = 0
					else:
						persenteks = jumlahteksporno/jumlahteks
					print persenteks
			except Exception as error:
				print(error)
			req = urllib2.Request(post_text, headers=hdr)
			cookiejar = cookielib.LWPCookieJar()
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
			try:
				page = urllib2.urlopen(req)
			except urllib2.HTTPError, e:
				print e.fp.read()
			page = urllib.urlopen(post_text)
			content = page.read()
			soup = BeautifulSoup(content)
			jmlgambar = len(soup.findAll('img'))
			print jmlgambar
			simpangambar = open("/usr/share/nginx/html/download/"+parsed+"/gambar.txt","w+")
			print >> simpangambar, ""
			for i in range(0,jmlgambar):
				gambars = ""
				try:
					gambars = soup.findAll('img')[i]['src']
					#print gambars
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
					simpangambar = open("/usr/share/nginx/html/download/"+parsed+"/gambar.txt","a+")
					print >> simpangambar, gambars
					print gambars
					linkgambar.append(gambars)
					filename = gambars.split("/")[-1]
					filename = filename.split("?")[0]
					outpath = os.path.join(out_gambar, filename)
					if (os.path.exists(outpath)):
						print "File sudah ada"
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
										gambarporno = ""
										if (float(pt)<0.45):
											gambarporno = subprocess.check_output(checkimage+os.path.splitext(outpath)[0]+".jpg",shell=True)
										elif (float(pt)>0.45):
											gambarporno = subprocess.check_output(checkimageporn+os.path.splitext(outpath)[0]+".jpg",shell=True)
										#gambarporno = subprocess.check_output(checkimage+os.path.splitext(outpath)[0]+".jpg",shell=True)
										if (str(1) in gambarporno):
											print "Gambar Porno"
											jumlahgambarporno.append(1)
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
					linkgambar.append(gambars)
					filename = gambars.split("/")[-1]
					filename = filename.split("?")[0]
					outpath = os.path.join(out_gambar, filename)
					if (os.path.exists(outpath)):
						print "File sudah ada"
						pass
					else:
						simpangambar = open("/usr/share/nginx/html/download/"+parsed+"/gambar.txt","a+")
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
										gambarporno = ""
										if (float(pt)<0.45):
											gambarporno = subprocess.check_output(checkimage+os.path.splitext(outpath)[0]+".jpg",shell=True)
										elif (float(pt)>0.45):
											gambarporno = subprocess.check_output(checkimageporn+os.path.splitext(outpath)[0]+".jpg",shell=True)
										#gambarporno = subprocess.check_output(checkimage+os.path.splitext(outpath)[0]+".jpg",shell=True)
										if (str(1) in gambarporno):
											print "Gambar Porno"
											jumlahgambarporno.append(1)
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
			totalgambar = n1 + n2 
			factor = float(g / h)
			n = n1+n2
			fbaru = 0
			print "Decision Factor: " + str(factor)
			fpembilang = ((((1 + p1 - p2)**n1) * ((1 + p2 - p1)**n2)) - ((p1 ** n1)*((1 - p1)**n2) * (((1-p1)+p2)**n))) * float(pt)
			#print fpembilang
			fpenyebut = ((2**n)-((1-p1+p2)**n)) * (p1**n1*((1-p1)**n2)) * (1-float(pt))
			#print fpenyebut
			if (fpenyebut>0):
				fbaru = float(fpembilang/fpenyebut)
			elif(fpenyebut==0):
				fbaru = factor
			#print fbaru
			if (pt>0.5 and n2>n1):
				p1 = 0.31 - n2 * pt
				p2 = 0.29 + n2 * pt
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
			totalgambar = n1 + n2 
			factor = float(g / h)
			fbaru = factor
			#print "Decision Baru " + str(fbaru) 
			if (pt>0.5 and n1==0 and n2==0):
				req = urllib2.Request(post_text, headers=hdr)
				cookiejar = cookielib.LWPCookieJar()
				opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
				try:
					page = urllib2.urlopen(req)
				except urllib2.HTTPError, e:
					print e.fp.read()
				page = urllib.urlopen(post_text)
				content = page.read()
				soup = BeautifulSoup(content)
				jmlgambar = len(soup.findAll('img'))
				print jmlgambar
				simpangambar = open("/usr/share/nginx/html/download/"+parsed+"/gambar.txt","w+")
				print >> simpangambar, ""
				for i in range(0,jmlgambar):
					gambars = ""
					try:
						gambars = soup.findAll('img')[i]['src']
						#print gambars
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
						gambars = domain + gambars
						simpangambar = open("/usr/share/nginx/html/download/"+parsed+"/gambar.txt","a+")
						print >> simpangambar, gambars
						print gambars
						linkgambar.append(gambars)
						filename = gambars.split("/")[-1]
						filename = filename.split("?")[0]
						outpath = os.path.join(out_gambar, filename)
						if (os.path.exists(outpath)):
							print "File sudah ada"
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
											gambarporno = ""
											if (float(pt)<0.45):
												gambarporno = subprocess.check_output(checkimage+os.path.splitext(outpath)[0]+".jpg",shell=True)
											elif (float(pt)>0.45):
												gambarporno = subprocess.check_output(checkimageporn+os.path.splitext(outpath)[0]+".jpg",shell=True)
											#gambarporno = subprocess.check_output(checkimage+os.path.splitext(outpath)[0]+".jpg",shell=True)
											if (str(1) in gambarporno):
												print "Gambar Porno"
												jumlahgambarporno.append(1)
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
						gambars = domain + gambars
						linkgambar.append(gambars)
						filename = gambars.split("/")[-1]
						filename = filename.split("?")[0]
						outpath = os.path.join(out_gambar, filename)
						if (os.path.exists(outpath)):
							print "File sudah ada"
							pass
						else:
							simpangambar = open("/usr/share/nginx/html/download/"+parsed+"/gambar.txt","a+")
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
											gambarporno = ""
											if (float(pt)<0.45):
												gambarporno = subprocess.check_output(checkimage+os.path.splitext(outpath)[0]+".jpg",shell=True)
											elif (float(pt)>0.45):
												gambarporno = subprocess.check_output(checkimageporn+os.path.splitext(outpath)[0]+".jpg",shell=True)
											#gambarporno = subprocess.check_output(checkimage+os.path.splitext(outpath)[0]+".jpg",shell=True)
											if (str(1) in gambarporno):
												print "Gambar Porno"
												jumlahgambarporno.append(1)
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
				n1 = float(sum(jumlahgambarporno))
				n2 = float(sum(jumlahgambartidakporno))
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
				totalgambar = n1 + n2 
				factor = float(g / h)
				n = n1+n2
				fbaru = 0
				print "Decision Factor: " + str(factor)
				fpembilang = ((((1 + p1 - p2)**n1) * ((1 + p2 - p1)**n2)) - ((p1 ** n1)*((1 - p1)**n2) * (((1-p1)+p2)**n))) * float(pt)
				#print fpembilang
				fpenyebut = ((2**n)-((1-p1+p2)**n)) * (p1**n1*((1-p1)**n2)) * (1-float(pt))
				#print fpenyebut
				if (fpenyebut>0):
					fbaru = float(fpembilang/fpenyebut)
				elif(fpenyebut==0):
					fbaru = factor
			#print "Decision Baru " + str(fbaru)
			if (pt<0.4 and n1>n2):
				p1 = 0.31 + n1 * (1-pt)
				p2 = 0.29 - n1 * pt
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
			totalgambar = n1 + n2 
			factor = float(g / h)
			fbaru = factor
			#print "Decision Baru " + str(fbaru)
			if (pt>0.5 and n1>n2 and persenteks<0.2):
				p1 = 0.31 - n1 * persenteks
				p2 = 0.29 + n1 * persenteks
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
			totalgambar = n1 + n2 
			factor = float(g / h)
			fbaru = factor
			#print "Decision Baru " + str(fbaru)
			if (pt>0.5 and n1>n2 and jumlahteks<100):
				p1 = 0.31 - n1 * persenteks
				p2 = 0.29 + n1 * persenteks
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
			totalgambar = n1 + n2 
			factor = float(g / h)
			fbaru = factor
			#print "Decision Baru " + str(fbaru)
			if (pt<0.5 and n1>n2 and (n1-n2)<=10):
				p1 = 0.31 - n1 * pt
				p2 = 0.29 + n2 * (1-pt)
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
			totalgambar = n1 + n2 
			factor = float(g / h)
			fbaru = factor
			#print "Decision Baru " + str(fbaru)
			if (pt>0.5 and n1>n2 and n1<=1 and n2==0 and jumlahteks<100):
				p1 = 0.31
				p2 = 0.29 + n1 * pt
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
			totalgambar = n1 + n2 
			factor = float(g / h)
			fbaru = factor
			#print "Decision Baru " + str(fbaru)
			if (pt<0.4 and n1>n2 and (n1-n2)<=5):
				p1 = 0.31 - n1 * (1-pt)
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
			totalgambar = n1 + n2 
			factor = float(g / h)
			fbaru = factor
			fbaru = abs(fbaru)
			print "Decision Baru " + str(fbaru)
			if (fbaru>=0.98):
				replacedText = ""
				textlist = []
				contentgabungan = ""
				print "Situs Porno"
				for gp in linkgambar:
					content = content.replace(gp,"http://202.169.224.53/stop.jpg")
					hasilsitus = open("/usr/share/nginx/html/download/"+parsed+"/hasilgambar.html","w+")
					print >> hasilsitus, content
				contentgabungan = BeautifulSoup(content)
				with open('talk/pornoList_Eng.txt','r') as f:
					for line in f:
						line = line.decode('unicode_escape').encode('ascii','ignore')
						line = line.rstrip('\r\n')
						textlist.append(line)
					#print textlist
				pattern = "r'(?i)|"+'|'.join(textlist)
				textPattern = re.compile(pattern)
				for t in contentgabungan.findAll(text=textPattern):
					t.replaceWith(re.sub(textPattern, "****", t))
					replacedText = basestring.__str__(contentgabungan)
				with open('talk/pornoList_Ind.txt','r') as f:
					for line in f:
						line = line.decode('unicode_escape').encode('ascii','ignore')
						line = line.rstrip('\r\n')
						textlist.append(line)
				pattern = "r'(?i)|"+'|'.join(textlist)
				textPattern = re.compile(pattern)
				for t in contentgabungan.findAll(text=textPattern):
					t.replaceWith(re.sub(textPattern, "****", t))
					replacedText = basestring.__str__(contentgabungan)
				#print replacedText
				hasilsitus = open("/usr/share/nginx/html/download/"+parsed+"/hasilgabungan.html","w+")
				print >> hasilsitus, replacedText
				response_data = {}
				response_data['decisionfactor'] = fbaru
				response_data['keputusan'] = "This site is contain negative text and image"
				response_data['hasil'] = "http://202.169.224.53/download/"+parsed+"/hasilgabungan.html"
				coll.insert({"url":post_text,"file":"http://202.169.224.53/download/"+parsed+"/hasilgabungan.html","status":"porn","factor":fbaru})
				collbaru.insert({"url":post_text,"file":"http://202.169.224.53/download/"+parsed+"/hasilgabungan.html","status":"porn","factor":fbaru})
				coll.insert({"url":post_text.replace('www.',''),"file":"http://202.169.224.53/download/"+parsed+"/hasilgabungan.html","status":"porn","factor":fbaru})
				collbaru.insert({"url":post_text.replace('www.',''),"file":"http://202.169.224.53/download/"+parsed+"/hasilgabungan.html","status":"porn","factor":fbaru})
				return HttpResponse(
					json.dumps(response_data),
					content_type="application/json"
				)
			else:
				print "Situs Tidak Porno"
				response_data = {}
				response_data['decisionfactor'] = fbaru
				response_data['keputusan'] = "This site doesn't contain negative text and image"
				response_data['hasil'] = post_text
				coll.insert({"url":post_text,"file":"http://202.169.224.53/download/"+parsed+"/hasilgabungan.html","status":"porn","factor":fbaru})
				collbaru.insert({"url":post_text,"file":"http://202.169.224.53/download/"+parsed+"/hasilgabungan.html","status":"porn","factor":fbaru})
				coll.insert({"url":post_text.replace('www.',''),"file":"http://202.169.224.53/download/"+parsed+"/hasilgabungan.html","status":"porn","factor":fbaru})
				collbaru.insert({"url":post_text.replace('www.',''),"file":"http://202.169.224.53/download/"+parsed+"/hasilgabungan.html","status":"porn","factor":fbaru})
				return HttpResponse(
					json.dumps(response_data),
					content_type="application/json"
				)
def video_process(request):
    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        jumlahteksporno = []
        listteksporno = []
        linkvideoporno = []
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
        req = urllib2.Request(post_text, headers=hdr)
        try:
            page = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e.fp.read()
        page = urllib.urlopen(post_text)
        br = mechanize.Browser()
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)
        br.set_handle_equiv(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        r = br.open(post_text)        
        content = page.read()
        #print content
        if "denied" in content:
        	content = r.read()
        #print content
        parsed = urlparse(post_text).netloc
        urlpath = urlparse(post_text).path
        urlpath = urlpath.replace("/",".")
        parsed = parsed.replace('www.','')
        parsed = parsed + str(urlpath)
        out_situs = "/usr/share/nginx/html/download/"+parsed
        if not os.path.exists(out_situs):
            os.mkdir(out_situs)
        soup = BeautifulSoup(content)
        videoxx = soup.find_all('video')
        for i in range(0,len(videoxx)):
            matches = re.search('src="([^"]+)"',repr(videoxx[i]))
            if repr(matches.group()):
                linkvideoporno.append(repr(matches.group()))
            else:
                pass
        iframexx = soup.find_all('iframe')
        for i in range(0,len(iframexx)):
            matches = re.search('src="([^"]+)"',repr(iframexx[i]))
            if repr(matches.group()):
                linkvideoporno.append(repr(matches.group()))
            else:
                pass
        embedxx = soup.find_all('embed')
        for i in range(0,len(embedxx)):
            matches = re.search('src="([^"]+)"',repr(embedxx[i]))
            if repr(matches.group()):
                linkvideoporno.append(repr(matches.group()))
            else:
                pass
        contentxx = soup.find('div', id=re.compile('.*content.*'))
        if contentxx:
            linkvideoporno.append(contentxx)
        else:
            pass
        videoxx = soup.find('div', class_=re.compile('.*video.*'))
        if videoxx:
            linkvideoporno.append(videoxx)
        else:
            pass
        print linkvideoporno
        for script in soup(["script", "style"]):
            script.extract()
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
        listtext = literal_eval(textlatest)
        print listtext
        try:
            classifier = Classify()
            output = classifier.predictBasedURL(post_text)
            hasil = output.get("class")
            print hasil
            if (hasil=="porno"):
                if linkvideoporno:
                    content = ("<html><center><img src='http://202.169.224.53/secsurf.png'></img><center></html>")
                hasilsitus = open("/usr/share/nginx/html/download/"+parsed+"/hasilvideo.html","w+")
                print >> hasilsitus, content
                response_data = {}
                response_data['keputusan'] = "This site is contain negative video"
                response_data['hasil'] = "http://202.169.224.53/download/"+parsed+"/hasilvideo.html"
                return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json"
                )
            elif (hasil=="tidak-porno"):
                response_data = {}
                response_data['keputusan'] = "This site doesn't contain negative video"
                response_data['hasil'] = post_text
                return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json"
                )
        except Exception as error:
            print(error)