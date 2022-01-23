from datetime import datetime

class Post:
    def __init__(self, date, body, url):
        self.date = datetime.strptime(date, "%A, %B %d, %Y %I:%M %p")
        self.body = body
        self.url = url
        
    def toJSON(self):
        return {
            "date" : self.date.strftime("%Y-%m-%d %H:%M:%S"),
            "body" : self.body,
            "url" : self.url
        }
    