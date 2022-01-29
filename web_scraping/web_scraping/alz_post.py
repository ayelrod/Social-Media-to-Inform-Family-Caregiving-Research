from datetime import datetime
from post import Post


class AlzPost(Post):
    """ AlzPost implements the Post class
        to represent a post on the
        www.alzconnected.org website
    """
    
    def __init__(self, date_string: str, title: str, body: str, reply: bool, user_name: str, user_date_joined_string: str, user_num_posts: int, url: str):
        """Constructor for the AlzPost class

        Args:
            date_string (str): The date/time the post was made
            title (str): The title of the post
            body (str): The text body of the post
            reply (bool): true if the post is a reply | false if the post is the original post
            user_name (str): The username of the poster
            user_date_joined_string (str): The date the poster joined the site
            user_num_posts (int): The number of posts the user has made
            url (str): The url where the post can be found
        """
        date = datetime.strptime(date_string, "%A %B %d %Y %I:%M %p")
        self.date = date
        self.title = title
        self.body = body
        self.reply = reply
        self.user_name = user_name
        self.user_date_joined = datetime.strptime(user_date_joined_string, "%m/%d/%Y")
        self.user_num_posts = user_num_posts
        self.url = url
        
    def toJSON(self):
        """Get the post in JSON form

        Returns:
            [dict]: The post in JSON form, represented by a Python dictionary
        """
        return {
            "date" : self.date.strftime("%Y-%m-%d %H:%M:%S"),
            "title" : self.title,
            "body" : self.body,
            "reply" : self.reply,
            "user_name" : self.user_name,
            "user_date_joined" : self.user_date_joined.strftime("%Y-%m-%d"),
            "user_num_posts" : self.user_num_posts,
            "url" : self.url
        }
        