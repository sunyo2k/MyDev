#coding:utf-8

import csv
try:
  from urllib.request import Request, urlopen,build_opener  # Python 3
  from urllib.error import HTTPError
except ImportError:
  from urllib2 import Request, urlopen, build_opener # Python 2
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

opener = build_opener()
opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')]

def get_title(url):
  try:
    html =  opener.open(url).read()
    soup = BeautifulSoup(html, "lxml")
    if soup.title is not None:
      if soup.title.string is not None:
        return soup.title.string
      else:
        return ""
    else:
      return ""
  except HTTPError as err:
    return "HTTPError:" + str(err.code)
  except OSError as err:
    return "OSError"

fr = open('urls.csv', 'r')
fw = csv.writer(open('urls_result.csv', 'a'))

data = csv.reader(fr)
for row in data:
  t = get_title(row[0])
  fw.writerow([row[0], t])
  print(row[0] + "	" + t)

