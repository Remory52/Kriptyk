import googlesearch as gs

class searchEngine():
    def makeQuery(query:str):
        results = [res for res in gs.search(query, "com", num=5, stop=5, pause=1.0)]
        return results[0]

    def isUrl(url):
        if "https" in url:
            return True
        return False