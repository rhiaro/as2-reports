import os
import urllib2
import json
from bs4 import BeautifulSoup, Tag
from markdown2 import Markdown, markdown_path

def init(features):
  page = BeautifulSoup("""<!doctype html>
<html>
  <head>
    <title>AS2 implemented features</title>
    <style type=\"text/css\">
      html { font-family: Arial }
      td, th {
        padding: 0.3em; margin: 0;
        border: 1px solid silver;
        text-align: center;
      }
    </style>
  </head>
  <body>
    <h1>AS2 implemented features</h1>
    <table></table>
  </body>
</html>""", 'html.parser')

  page = list_features(page, features)
  return page

def list_features(page, features):

  first = add_row(page)
  add_col(page, first, "th", "Feature / Implementation")
  for f in features:
    r = add_row(page)
    add_col(page, r, "th", f)

  return page

def get_features():
  request = urllib2.Request("https://www.w3.org/ns/activitystreams", headers={"Accept" : "application/ld+json"})
  contents = urllib2.urlopen(request).read()
  l = json.loads(contents)["@context"].keys()
  l.remove("xsd")
  l.remove("@vocab")
  l.remove("id")
  l.remove("type")
  l.remove("ldp")
  return sorted(l)

def add_row(page):
  table = page.table
  row = page.new_tag("tr")
  table.append(row)

  return row

def add_col(page, row, tag, string):
  cell = page.new_tag(tag)
  cell.append(string)
  row.append(cell)

  return row

def parse_reports():

  features = get_features()
  page = init(features)
  rows = page.table.find_all('tr')
  row = 0
  first = rows[row]

  path = os.getcwd()+"/activitystreams/implementation-reports/"

  for filename in os.listdir(path):
    row = 0
    if filename != "template.md":
      html = markdown_path(path+filename)
      soup = BeautifulSoup(html, 'html.parser')

      imp_name = soup.h1.string
      add_col(page, first, "th", imp_name)

      if(row < len(features)):
        for f in features:
          row = row + 1
          next_row = rows[row]
          if(is_implemented(f, soup)):
            add_col(page, next_row, "td", "X")
          else:
            add_col(page, next_row, "td", "")

  return page

def is_implemented(feature, implementation_soup):
  
  classes = implementation_soup.find_all('h3')
  properties = implementation_soup.find_all('li')

  for c in classes:
    if c.string == feature:
      answer = c.next_sibling
      if answer == "\n":
        answer = answer.next_sibling
      
      if answer and answer.string[15] == "y":
        return True
      else:
        return False

  for p in properties:
    
    answer = p.string.split(": ")
    if answer[0] == feature:
      if answer[1] and answer[1][0] == "y":
        return True
      else:
        return False

def write(html):
  if not os.path.exists(os.getcwd()+"/out"):
    os.makedirs(os.getcwd()+"/out")

  with open(os.getcwd()+"/out/reports.html", "w+") as the_file:
    the_file.write(html)

page = parse_reports()
write(page.prettify())