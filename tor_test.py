import urllib2
proxy = urllib2.ProxyHandler({'http': '127.0.0.1:8118'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)
print urllib2.urlopen('http://icanhazip.com/').read()


proxy = urllib2.ProxyHandler({'http': '127.0.0.1:8118'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)
print urllib2.urlopen('http://icanhazip.com/').read()