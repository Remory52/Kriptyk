import googlesearch as gs
from requests import get
from youtube_dl import YoutubeDL

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True', 'quiet':True}

class searchEngine():
    def makeQuery(query:str):
        results = [res for res in gs.search(query, num_results=5)]
        return results[0]

    def isUrl(url):
        if "https" in url:
            return True
        return False

    def search(arg):
        with YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                get(arg) 
            except:
                video = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
            else:
                video = ydl.extract_info(arg, download=False)

        return (video['title'], video['url'])