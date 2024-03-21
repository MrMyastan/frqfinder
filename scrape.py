from bs4 import BeautifulSoup
from urllib import request
from pprint import pprint
import json
import requests
from os import path
import os

url = "https://apcentral.collegeboard.org/courses/ap-calculus-bc/exam/past-exam-questions"
req = request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
page = request.urlopen( req )
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

containers = soup.find_all("div", class_="cb-accordion-container")

form_a = {}
form_b = {}

for container in containers:
    year, form = container.find("span").string.strip().split(": ")
    if year == "2020":
        continue
    destination = form_a
    if form == "Form B":
        destination = form_b
    
    link = container.find("a", string="Scoring Guidelines").get("href")
    if link[0] == "/":
        link = "https://apcentral.collegeboard.org" + link

    destination[year] = link

links_bc = {"A": form_a, "B": form_b}

url = "https://apcentral.collegeboard.org/courses/ap-calculus-ab/exam/past-exam-questions"
req = request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
page = request.urlopen( req )
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

containers = soup.find_all("div", class_="cb-accordion-container")

form_a = {}
form_b = {}

for container in containers:
    year, form = container.find("span").string.strip().split(": ")
    if year == "2020":
        continue
    destination = form_a
    if form == "Form B":
        destination = form_b
    
    link = container.find("a", string="Scoring Guidelines").get("href")
    if link[0] == "/":
        link = "https://apcentral.collegeboard.org" + link

    destination[year] = link

links_ab = {"A": form_a, "B": form_b}

links = {"AB": links_ab, "BC": links_bc}

with open("links.json", "w") as f:
    f.write(json.dumps(links))

FOLDER = "FRQs"

for tn,test in links.items():
    for fn, form in test.items():
        for year,link in form.items():
            fpath = path.join(FOLDER, tn,year)
            os.makedirs(fpath,exist_ok=True)
            blob = requests.get(link).content
            with open(path.join(fpath,f"{fn}.pdf"),'wb') as f:
                f.write(blob)