from datetime import datetime
from post import Post


class AlzPost(Post):
    def __init__(self, date_string, body, url):
        date = datetime.strptime(date_string, "%A, %B %d, %Y %I:%M %p")
        super().__init__(date, body, url)
        