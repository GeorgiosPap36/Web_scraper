from sys import argv
import requests
from bs4 import BeautifulSoup


def GetScriptPath():
    global path
    temp = argv[0].split("/")
    pathList = temp[:len(temp) - 1]
    for word in pathList:
        path = path + word + "\\"

def EditText(command, text, name):
    with open(path + "\\" + name + ".txt", command, encoding="utf-8") as myFile:
        myFile.write(text)

path = ""
GetScriptPath()

URL = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

result = soup.find(id = "pagecontent")
result = result.find(id = "main")
result = result.find("div", class_ = "article")
result = result.find("span", class_ = "ab_widget")
result = result.find("div", class_ = "seen-collection")
result = result.find("div", class_ = "article")
result = result.find("div", class_ = "lister")
result = result.find("table", class_ = "chart full-width")
result = result.find("tbody", class_ = "lister-list")

trs = result.find_all("tr")

for i in range(1, len(trs)):
    current_tr = trs[i].find("td", class_ = "titleColumn")
    temp = current_tr.find_all("a", href = True)
    movieLink = temp[0]["href"]

    EditText("a+", "www.imdb.com" + movieLink + "\n", "MovieLink")