# google kewords search for pythonista
# coding: utf-8
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import codecs
import datetime
import re
import time

keywords = ["airplane","news", "python"]

def google_rank(kw):
  url="https://www.google.co.jp/search?num=100&q=" + urllib.parse.quote_plus(kw, encoding='utf-8')
  #url="https://www.google.co.jp/search?q=" + urllib.parse.quote_plus(kw, encoding='utf-8')

  opener = urllib.request.build_opener()
  opener.addheaders = [('User-agent', 'Mozilla/5.0')]

  html = opener.open(url)
  soup = BeautifulSoup(html.read(), "html.parser")

  a = []
  for i, h3 in enumerate(soup.findAll("h3",{"class":"r"})):
    urlstr = h3.a['href']
    if re.match(r'\/url\?q=.*', urlstr) is not None:
      tmp = urllib.parse.parse_qs(urllib.parse.urlparse(urlstr).query)
      urlstr = tmp['q'][0]

#    row = [datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S"),
    row = [kw,
           str(i+1),
           urlstr,
           h3.a.get_text()]
    a.append(row)
    if i == 0 or re.search(r'google\.co\.jp|google\.com', urlstr) is not None:
      print(row)

for kw in keywords:
  google_rank(kw)
  time.sleep(2)
