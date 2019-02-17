#!C:\Python20 python

from sys import argv
from os import makedirs, unlink
from os.path import dirname, exists, isdir, splitext
from string import replace, find, lower
from htmllib import HTMLParser
from urllib import urlretrieve
from urlparse import urlparse, urljoin
from formatter import DumbWriter, AbstractFormatter
from cStringIO import StringIO

class Retriever(htmllib.HTMLParser): #download Web Pages
	
	def __init__(self, url):
		self.url = url
		self.file = self.filename(url)

	def filename(self, url, deffile='index.htm'):
		parsedurl = urlparse(url,'http:',0) #parse path
		path = parsedurl[1] + parsedurl[2]
		text = splitext(path)
		if text[1]=='': #its not file use default
			if text[-1] == '/':
				path = path + deffile
			else:
				path = path + '/' + deffile
		print "PATH:%s" % path
		dir = dirname(path)
		if not isdir(dir): #create new archieve dir if necessary
			if exists(dir): unlink(dir)
			makedirs(dir)
		return path
	
	def download(self): #download web pages
		try:
			retval = urlretrieve(self.url,self.file)
		except IOError:
			retval =('***ERROR: invalid URL "%s"' % self.url)
		
		return retval
	def parseAndGetLinks(self): #Parse HTML
		self.parser = HTMLParser(AbstractFormatter(\
				DumbWriter(StringIO())))
		self.parser.feed(open(self.file).read())
		self.parser.close()
		return self.parser.anchorlist


class Crawler: 
	count = 0 
	
	def __init__(self,url):
		self.q = [url]
		self.seen = []
		self.dom = urlparse(url)[1]

	def getPage(self,url):
		r = Retriever(url)
		retval = r.download()
		if retval[0]=='*': #error dont parse
			print retval,'....Skipping parser'
			return
		Crawler.count = Crawler.count + 1
		print '\n(',Crawler.count, ')'
		print 'URL:', url
		print 'FILE:', retval[0]
		self.seen.append(url)

		links = r.parseAndGetLinks() 
		for eachLink in links:
			if eachLink[:4]!= 'http' and find(eachLink, '://')==-1:
				eachLink = urljoin(url,eachLink)
			print '* ',eachLink,

			if find(lower(eachLink),'mailto:')!= -1:
			   print '....discarded, mailto link'
			   continue
			
			if eachLink not in self.seen:
				if find(eachLink, self.dom) == -1:
					print '..discarded not in domain'
				else:
					if eachLink not in self.q:
					  self.q.append(eachLink)
					  print '...new , added to Q'
					else:
					  print '...discarded already in Q'
			else:
			   print '...discarded, already processed'
		
	def go(self): # process links in queue
			while self.q:
				url = self.q.pop()
				self.getPage(url)

def main():	
	url = raw_input("Enter URL:")
	robot = Crawler(url)
	robot.go()

if __name__ == '__main__':
	main()
			  
		






