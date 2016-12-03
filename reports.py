import os
from bs4 import BeautifulSoup
from markdown2 import Markdown, markdown_path

def parse_report():

  path = os.getcwd()+"/activitystreams/implementation-reports/"
  for filename in os.listdir(path):
    html = markdown_path(path+filename)
    soup = BeautifulSoup(html, 'html.parser')

    print soup.h1.string

print parse_report()