import os
from bs4 import BeautifulSoup, Tag
from markdown2 import Markdown, markdown_path

def init():
  page = BeautifulSoup("", 'html.parser')
  html = page.new_tag("html")
  table = page.new_tag("table")

  page.append(html)
  html.append(table)

  page = list_features(page)

  return page

def list_features(page):
  first = add_row(page)

  classes = get_classes()
  properties = get_properties()

  for c in classes:
    add_col(page, first, "th", c)

  for p in properties:
    add_col(page, first, "th", p)

  return page

# TODO: get from namespace
def get_classes():
  return ["Activity", "Object", "Like"]

def get_properties():
  return ["object", "target", "published"]

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

  page = init()
  path = os.getcwd()+"/activitystreams/implementation-reports/"

  classes = get_classes()
  properties = get_properties()
  features = classes + properties

  for filename in os.listdir(path):
    html = markdown_path(path+filename)
    soup = BeautifulSoup(html, 'html.parser')

    imp_name = soup.h1.string
    tr = add_row(page)
    add_col(page, tr, "th", imp_name)

    for f in features:
      if(is_implemented(f, soup)):
        add_col(page, tr, "td", "X")
      else:
        add_col(page, tr, "td", "")

  return page

def is_implemented(feature, implementation_soup):
  return True

def write(html):
  if not os.path.exists(os.getcwd()+"/out"):
    os.makedirs(os.getcwd()+"/out")

  with open(os.getcwd()+"/out/reports.html", "a+") as the_file:
    print the_file.write(html)

page = parse_reports()
write(page.prettify())