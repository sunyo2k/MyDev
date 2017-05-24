# coding: utf-8
import requests
import xml.etree.ElementTree as ET

countries = {"kr":"p23", "us":"p1", "jp":"p4", "uk":"p9"}
ns = {"ht":"https://trends.google.com/trends/hottrends","atom":"http://www.w3.org/2005/Atom"}

for k in countries:
  handle = countries[k]
  link = "https://www.google.com/trends/hottrends/atom/feed?pn=" + handle
  root = ET.fromstring(requests.get(link).text)
  for channel in root.findall('channel'):
    i = 0
    for item in channel.findall('item'):
      i += 1
      title = item.find('title')
      traffic = item.find('ht:approx_traffic',ns)
      link = item.find('link')
      print(k, i, title.text, traffic.text)
