from sys import argv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from currency_converter import CurrencyConverter


def GetScriptPath():
    global path
    temp = argv[0].split("/")
    pathList = temp[:len(temp) - 1]
    for word in pathList:
        path = path + word + "\\"

def EditText(command, text, name):
    with open(path + "\\" + name + ".txt", command) as myFile:
        myFile.write(text)

def GetName(htmlPart):
    movieName = htmlPart.find("h1").getText()
    movieName = movieName.split("(")[0].strip()
    return movieName

def GetDuration(htmlPart):
    temp = htmlPart.find("time").getText().strip()
    hours = 0
    minutes = 0
    if "h" in temp:
        temp = temp.split()
        try:
            hours = int(temp[0].split("h")[0])
        except:
            hours = 0

        try:
            minutes = int(temp[1].split("m")[0])
        except:
            minutes = 0
    else:
        try:
            minutes = int(temp.split("m")[0])
        except:
            minutes = 0

    duration = hours * 60 + minutes
    return duration

def GetGenresList(htmlPart):
    subtexts = htmlPart.find_all("a")
    temp = subtexts[:-1]
    genres = []
    for genre in temp:
        genres.append(genre.getText())
    return genres

def GetReleaseYear(htmlPart):
    subtexts = htmlPart.find_all("a")
    temp = subtexts[-1].getText().split()
    year = int(temp[-2])
    return year

def GetAgeRating(htmlPart):
    temp = htmlPart.getText().split()[0]
    rating = temp
    if rating == "Not":
        rating = "None"
    return rating

def GetDirector(htmlPart):
    temp = htmlPart[0].getText()
    temp = temp.split(":")[1]
    try:
        temp = temp.split(",")
        director = temp[0]
    except ValueError:
        director = temp.strip()
    director = director.replace("\n", "")
    return director

def GetStars(htmlPart):
    temp = htmlPart[-1].getText().strip().split("|")
    temp = temp[0]
    temp = temp.split(":")[1]
    temp = temp.split(",")
    stars = []
    for item in temp:
        stars.append(item.strip())
    return stars

def ConverCurrencyToUSD(currencyStr):
    c = CurrencyConverter()
    if currencyStr.find("$") != -1:
        currencyStr = currencyStr.replace("$", "USD")
    currency = currencyStr[0:3].strip()
    value = int(currencyStr[3:].replace(",", ""))
    try:
        final = c.convert(value, currency, "USD")
        final = float("{:.2f}".format(final))
    except:
        final = currencyStr
    return final

def GetBudget(htmlPart):
    temp = "None"
    budget = "None"
    for item in htmlPart:
        if item.getText().find("Budget:") != -1:
            temp = item.getText()
            break
    if temp != "None":
        temp = temp.split(":")[1]
        temp = temp.split("(")[0]
        temp = temp.strip()
        budget = ConverCurrencyToUSD(temp)

    return budget

def GetGrossRevenue(htmlPart):
    temp = "None"
    revenue = "None"
    for item in htmlPart:
        if item.getText().find("Cumulative Worldwide Gross:") != -1:
            temp = item.getText()
            break
    
    if temp != "None":
        temp = temp.split(":")[1].strip()
        revenue = ConverCurrencyToUSD(temp)

    return revenue

def GetCountry(htmlPart):
    temp = "None"
    for item in htmlPart:
        if item.getText().find("Country:") != -1:
            temp = item.getText()
            break
    temp = temp.split(":")[1]
    try:
        temp = temp.split("|")
        country = temp[0].strip()
    except ValueError:
        country = temp 
    return country

def GetRating(htmlPart):
    temp = htmlPart.find("div", class_ = "ratingValue")
    rating = float(temp.getText().split("/")[0].strip())
    return rating

def GetMovieStats(URL):
    options = Options()
    options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\Chrome.exe"
    driver = webdriver.Chrome(chrome_options=options, executable_path= "C:\\Users\\kseft\\Desktop\\CS\\Python\\ChromeDriver\\chromedriver.exe", )
    driver.get(URL)

    time.sleep(2)
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, "html.parser")
    titleBlock = soup.find("div", id = "title-overview-widget", class_ = "heroic-overview")

    print("Initiating Extraction Sequence")
    print("------------------------------")

    result = titleBlock.find("div", class_ = "title_wrapper")
    movieName = GetName(result)

    subtext = result.find("div", class_ = "subtext")
    movieDuration = GetDuration(subtext)
    movieAgeRating = GetAgeRating(subtext)
    movieReleaseYear = GetReleaseYear(subtext)
    movieGenres = GetGenresList(subtext)
    movieRating = GetRating(titleBlock)
    
    mainBottom = soup.find("div", id = "main_bottom", class_ = "main")
    moreBottom = mainBottom.find("div", class_ = "article", id = "titleDetails")
    textBlocks = moreBottom.find_all("div", class_ = "txt-block")
    movieCountry = GetCountry(textBlocks)
    movieBudget = GetBudget(textBlocks)
    movieRevenue = GetGrossRevenue(textBlocks)

    plotSummary = titleBlock.find("div", class_ = "plot_summary_wrapper")
    plotSummary = plotSummary.find_all("div", class_ = "credit_summary_item")
    director = GetDirector(plotSummary)
    starsList = GetStars(plotSummary)


    lineInTxt = movieName + " - " + str(movieDuration) + " - " + str(movieAgeRating) + " - " + str(movieRating) + " - " + str(movieBudget) + " - " + str(movieRevenue) + " - " + str(movieReleaseYear) + " - " + movieCountry
    for genre in movieGenres:
        lineInTxt = lineInTxt + " - " + genre
    lineInTxt = lineInTxt + " - " + director
    for star in starsList:
        lineInTxt = lineInTxt + " - " + star
    lineInTxt = lineInTxt + "\n"
    print(lineInTxt)

    driver.close()

    print("------------------------------")
    print("Extraction Sequence Completed")
    return lineInTxt

def FunctionToRuleThemAll():
    movieLinksTxt = open(path + "MovieLink.txt")
    movieLinks = movieLinksTxt.readlines()
    movieLinksTxt.close()
    for i in range(29, len(movieLinks)):
        print(i)
        EditText("a+", GetMovieStats("https://" + movieLinks[i]), "MovieStats")
    
path = ""
GetScriptPath()
#FunctionToRuleThemAll()
GetMovieStats("https://www.imdb.com/title/tt4016934/")
#GetMovieStats("https://www.imdb.com/title/tt0110413/")