from datetime import datetime

class Post:
    def __init__(self, date, body, url):
        self.date = date
        self.body = body
        self.url = url
        
    def toJSON(self):
        return {
            "date" : self.date.strftime("%Y-%m-%d %H:%M:%S"),
            "body" : self.body,
            "url" : self.url
        }
        
    def writeToDatabase(self):
        # TODO: Write post to database
        pass
    