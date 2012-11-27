import sys
from HTMLParser import HTMLParser

class ParseHTML(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = 0

    def handle_starttag(self, tag, attrs):
        #print "Encountered the beginning of a %s tag" % tag
        if tag =="p":
            self.flag = 1
    def handle_data(self,data):
        if self.flag == 1:
	    s = data.replace(' ', '').replace('\r', '').replace('\t', '').replace('\n', '')
	    if len(s) > 0:
		print s
		self.flag=0

def test(filename):
    html = open(filename).read()
    parser = ParseHTML()
    parser.feed(html)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        test(sys.argv[1])

