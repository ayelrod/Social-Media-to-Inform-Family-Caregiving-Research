from datetime import datetime
from post import Post


class AlzPost(Post):
    """ AlzPost implements the Post class
        to represent a post on the
        www.alzconnected.org website
    """
    
    def __init__(self, date_string: str, body: str, url: str):
        """Constructor for the AlzPost class

        Args:
            date_string (str): The date/time the post was made
            body (str): The text body of the post
            url (str): The url where the post can be found
        """
        date = datetime.strptime(date_string, "%A, %B %d, %Y %I:%M %p")
        self.date = date
        self.body = body
        self.url = url
        
    def toJSON(self):
        """Get the post in JSON form

        Returns:
            [dict]: The post in JSON form, represented by a Python dictionary
        """
        return {
            "date" : self.date.strftime("%Y-%m-%d %H:%M:%S"),
            "body" : self.body,
            "url" : self.url
        }
        