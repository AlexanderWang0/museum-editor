import json
import os
import requests
#import shutil
import sys
import urllib.request
#from bs4 import BeautifulSoup

buildHTML = "<li><a href=\"https://github.com/WolverineSoft/museum/releases/latest/download/fileName\">buildType</a></li>\n"
buildTypes = ["Mac Version", "Windows Version", "Linux Version", "Android Version", "Web Version"]

def getBetween(string, start, end):
    output = string[string.index(start) + len(start):]
    return output[0:output.index(end)]

def getAllBetween(string, start, end):
    output = []
    #print(start)
    
    while(start in string and end in string):
        #if("Hi Austin" in string):
            #allDebug = open("allDebug.txt", "w")
            #allDebug.write(string)
            #print("wrote debug output")
            
        string = string[string.index(start) + len(start):]
        output.append(string[0:string.index(end)])
        string = string[string.index(end) + 1:]
        
    return output

def removeBetween(string, start, end):
    while(start in string and end in string):
        startIndex = string.index(start)
        afterStart = string[startIndex + 1:]
        
        if(not end in afterStart):
            break
        
        string = string[0:startIndex] + afterStart[afterStart.index(end) + 1:]
    
    return string

def removeTags(string):
    while("<" in string):
        afterLess = string[string.index("<"):]
        
        if(not ">" in afterLess):
            return string
        
        string = string[0:string.index("<")] + " " + afterLess[afterLess.index(">") + 1:]
    
    string = string.replace("\n", " ").replace("\r", " ")
    
    while("  " in string):
        string = string.replace("  ", " ")
    
    return string

debug = open("debug.txt", "w")
inFile = open("csv/" + sys.argv[1], "r")
firstLine = True
allgamesFile = open("museum/allgames.js", "r")
allgamesString = allgamesFile.read()
allgamesString = allgamesString[allgamesString.index("\n") + 1:-3].replace("title:", "\"title\":").replace("img:", "\"img\":").replace("year:", "\"year\":").replace("desc:", "\"desc\":").replace("type:", "\"type\":") + "\n}"
#debug.write(allgamesString)
allgames = json.loads(allgamesString)
#debug.write(json.dumps(allgames, indent=4))
gameYear = "".join([a for a in sys.argv[1] if (a in "0123456789")])

if(0 == len(gameYear)):
    gameYear = "2023"
elif(2 == len(gameYear)):
    gameYear = "20" + gameYear
elif(4 != len(gameYear)):
    print(gameYear + "'s length isn't valid.")

for a in inFile:
    if(firstLine):
        #gameYear = a.replace("\n", "")
        firstLine = False
        continue
    
    inputs = a.replace("\n", "").split(",")
    gameName = inputs[1]
    itchURL = inputs[3]
    game = itchURL[itchURL.index(".itch.io/") + len(".itch.io/"):]
    path = "museum/" + game
    response = requests.get(itchURL, headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0"})
    html = response.text
    print(game)
    
    if("<h2 id=\"download\">Download</h2><div class=\"buy_row\"><p>This game is currently unavailable</p>" in html or 404 == response.status_code):
        continue
    #debug.write(html)
    #soup = BeautifulSoup(request.content, "html5lib")
    #debug.write(soup.prettify())
    indexTemplate = open("index.html", "r")
    indexText = indexTemplate.read()
    authorBlock = getBetween(html, "<td>Author", "</tbody>")
    
    if("<td>Genre</td>" in html):
        authorBlock = getBetween(html, "<td>Author", "<td>Genre</td>")
        
    authorList = getAllBetween(authorBlock, ".io\">", "</a>")
    gameAuthors = authorList[0]
    gameDescription = ""
    gameDescriptionLink = "<a href=\"" + itchURL + "\">Itch.io page</a>"
    
    if("user_formatted\">" in html):
        html = removeBetween(html, "class=\"post_content\"", "</div>")
        gameDescriptionList = getAllBetween(html, "user_formatted\">", "</div>")
        #print("game: " + game + ", game description sections: " + str(len(gameDescriptionList)))
        
        for a in range(0, len(gameDescriptionList)):
            gameDescription = gameDescription + gameDescriptionList[a]
            gameDescription = gameDescription + "\n"
        
        gameDescriptionLink = gameDescription + "<a href=\"" + itchURL + "\">Itch.io page</a>"
    
    for b in range(1, len(authorList)):
        gameAuthors = gameAuthors + ", " + authorList[b]
    
    #print(gameYear)
    indexText = indexText.replace("gameName", gameName).replace("gameYear", gameYear).replace("gameDescription", gameDescriptionLink).replace("gameAuthors", gameAuthors)
    gameBuilds = ""
    hasDifferentBuilds = False
    inputs[9], inputs[10] = inputs[10], inputs[9]

    for b in range(0, 4):
        fileName = inputs[b + 9].replace(" ", ".").replace("&", ".")
        
        while(".." in fileName):
            fileName = fileName.replace("..", ".")
    
        if(0 < len(fileName)):
            if(1 == b and inputs[9] == inputs[10]):
                gameBuilds = buildHTML.replace("fileName", fileName).replace("buildType", "Mac and Windows Version")
                continue
            
            #if(4 == b):
                #fileName = game + "-web.zip"
            #print(len(fileName))
            #print("not a variable")
            #shutil.copy2("downloads/" + fileName, path)
            gameBuilds = gameBuilds + buildHTML.replace("fileName", fileName).replace("buildType", buildTypes[b])
    
    if("" == gameBuilds and "/index.html" in html):
        gameBuilds = "This game runs in browser only."
    else:
        gameBuilds = "<ul>\n" + gameBuilds + "</ul>"
    
    indexText = indexText.replace("gameBuilds", gameBuilds)
    
    try:
        os.mkdir(path)
    except FileExistsError:
        print("caught FileExistsError")
    
    if(not itchURL in allgames.keys()):
        allgames[game] = {}
    
    allgames[game]["title"] = gameName
    allgames[game]["img"] = ""
    allgames[game]["year"] = int(gameYear)
    allgames[game]["desc"] = removeTags(gameDescription).strip()
    allgames[game]["type"] = "jam"
    
    if("/original/" in html):
        originalIndex = html.index("/original/")
        urllib.request.urlretrieve(html[html[0:originalIndex].rindex("\"") + 1:html[originalIndex:].index("\"") + originalIndex], path + "/thumbnail.png")
        allgames[game]["img"] = game + "/thumbnail.png"
    else:
        indexText = indexText.replace("      <img class=\"gameHero\" src=\"thumbnail.png\">\n", "")
    
    index = open(path + "/index.html", "w")
    index.write(indexText)
    
#debug.write(html)
#debug.write(json.dumps(allgames, indent=4))
allgamesOutFile = open("museum/allgames.js", "w")
allgamesOutFile.write("const allgames = \n" + json.dumps(allgames, indent=4).replace("\"title\":", "title:").replace("\"img\":", "img:").replace("\"year\":", "year:").replace("\"desc\":", "desc:").replace("\"type\":", "type:")[0:-2] + ",\n}")
