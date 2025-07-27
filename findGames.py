import os
import requests

def getBetween(string, start, end):
    output = string[string.index(start) + len(start):]
    return output[0:output.index(end)]

def downloadAllGames(url):
    gamePages = []
    folderName = url[url.rindex('/') + 1:]
    entriesSource = requests.get(url + "/entries").text
    gameSection = getBetween(entriesSource, "<div class=\"index_game_grid_widget preview_grid\">", "<div class=\"loading_container\">")
    os.mkdir(folderName)
    print(gameSection)
    
    while("<div class=\"bordered\"><a href=\"" in gameSection):
        #print(gameSection)
        gamePages.append(getBetween(gameSection, "<div class=\"bordered\"><a href=\"", "\" class="))
        print(gamePages[-1])
        startIndex = gameSection.index("game_thumb") + 1
        gameSection = gameSection[startIndex:]
    
    for a in gamePages:
        print(a)
        gameFolderName = a[a.index(".io/") + 4:]
        os.mkdir(folderName + '/' + gameFolderName)
        source = requests.get(a).text
        html = open(folderName + '/' + gameFolderName + '/' + gameFolderName + ".html", 'w')
        html.write(source)

def downloadURLList(gamePages, folderName):
    for a in gamePages:
        print(a)
        gameFolderName = a[a.index(".io/") + 4:]
        os.mkdir(folderName + '/' + gameFolderName)
        source = requests.get(a).text
        html = open(folderName + '/' + gameFolderName + '/' + gameFolderName + ".html", 'w')
        html.write(source)

#downloadAllGames("https://itch.io/jam/wsoft-shammy-jam-2020")
downloadURLList(["https://hardboiledstudios.itch.io/back-2-back", "https://musahaydar.itch.io/awake-and-away", "https://gracewqma.itch.io/saving-grace", "https://ruidong.itch.io/and-then-there-were-two", "https://yizhou616.itch.io/whenyoureforcedtopivotfrommultiplayerintosomethingelsesothisiswhatyouhavetoresor", "https://tobyaaa.itch.io/short-platformer", "https://nixl.itch.io/two-boxes"], "wsoft-shammy-jam-2020")
#https://docs.google.com/document/d/1404a0I1XVkTLpHErylHlrt7Sj372a5y0yY8gyy1kba8/edit
#https://itchio-mirror.cb031a832f44726753d6267436f3b414.r2.cloudflarestorage.com/upload2/game/456557/1558500?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=3edfcce40115d057d0b5606758e7e9ee%2F20250121%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20250121T080531Z&X-Amz-Expires=60&X-Amz-SignedHeaders=host&X-Amz-Signature=86de6b74ef9093f887638566d0d0a44f80a31520f516a2c740651d58c10963ce
#https://itchio-mirror.cb031a832f44726753d6267436f3b414.r2.cloudflarestorage.com/upload2/game/456557/1558500?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=3edfcce40115d057d0b5606758e7e9ee%2F20250121%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20250121T081310Z&X-Amz-Expires=60&X-Amz-SignedHeaders=host&X-Amz-Signature=ca55699e8e7419f9c116a5d24cda69949f9999996a7aa557d64601e7084c921b
#https://itchio-mirror.cb031a832f44726753d6267436f3b414.r2.cloudflarestorage.com/upload2/game/456557/1558500?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=3edfcce40115d057d0b5606758e7e9ee%2F20250121%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20250121T090531Z&X-Amz-Expires=60&X-Amz-SignedHeaders=host&X-Amz-Signature=86de6b74ef9093f887638566d0d0a44f80a31520f516a2c740651d58c10963ce
