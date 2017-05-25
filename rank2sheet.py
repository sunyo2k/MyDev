# coding: utf-8
# get search keyword ranks
import requests
import urllib.parse
from bs4 import BeautifulSoup
import sys, re, datetime, time
from pprint import pprint
# write spread sheet 
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

# preparation
# python library, google api setup, spread sheet 

# get search keyword ranks
keywords = ["ニュース","自動車保険", "英会話", "ネット証券"]

# write spreadsheet 
G_SHEET_ID = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
G_SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
G_SERCRET = "xxxxxxxxxxxxxxxxxxxx.json"


def get_rank(keyword):
  #link = "https://www.google.co.jp/search?num=10&q=" + keyword
  link = "https://www.google.co.jp/search?num=100&q=" + keyword
  html = requests.get(link).text
  if not html:
    print("no response on request")
    sys.exit()
  else:
    soup = BeautifulSoup(html, "html.parser")

  a = list()
  for i, h3 in enumerate(soup.findAll("h3",{"class":"r"})):
    urlstr = h3.a['href']
    if re.match(r'\/url\?q=.*', urlstr) is not None:
      tmp = urllib.parse.parse_qs(urllib.parse.urlparse(urlstr).query)
      urlstr = tmp['q'][0]
    elif re.match(r'\/search\?q=.*', urlstr) is not None:
      urlstr = "https://www.google.co.jp/"
    row = [str(i+1),
           h3.a.get_text(),
           urlstr,
           datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")]
    a.append(row)

  return a


def write_sheet(keyword, rows):
  credentials = ServiceAccountCredentials.from_json_keyfile_name(G_SERCRET, G_SCOPES)
  service = discovery.build('sheets', 'v4', credentials=credentials)
  spreadsheet_id = G_SHEET_ID

  rangeName = keyword + '!A1:A'
  result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=rangeName).execute()
  values = result.get('values', [])
  curRowsLen =len(values)

  if not values:
    print('sheet has no data')

  batch_update_values_request_body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
      {
        "range": keyword + "!A" + str(curRowsLen+1) + ":E" + str(curRowsLen + len(rows)),
        "majorDimension": "ROWS",
        "values": rows
      }
    ]
  }

  #pprint(batch_update_values_request_body)
  request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id,body=batch_update_values_request_body)
  response = request.execute()

  # TODO: Change code below to process the `response` dict:
  pprint(response)
  return response

def main():

  for keyword in keywords:
    # get rank list
    a = get_rank(keyword)

    # write to spreadsheet
    write_sheet(keyword, a)
  
if __name__ == "__main__":
  main()

