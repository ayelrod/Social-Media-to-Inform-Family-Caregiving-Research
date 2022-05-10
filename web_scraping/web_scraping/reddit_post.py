from datetime import datetime
from post import Post
from urllib.parse import urlparse
from urllib.parse import parse_qs
from mongoDB import MongoDB
# import pymongo

# GLOBAL VARIABLE
database = MongoDB() # Create connection to database

class RedditPost(Post):
    """ RedditPost implements the Post class
        to represent a post on reddit
    """
    
    def __init__(self, post_id: str, date_string: str, title: str, body: str, num_upvotes: int, num_downvotes: int, reply: bool, user_name: str, url: str):
        """Constructor for the RedditPost class

        Args:
            post_id (str): The id of the post
            date_string (str): The date/time the post was made
            title (str): The title of the post
            body (str): The text body of the post
            num_upvotes (int): The number of upvotes on the post
            num_downvotes (int): The number of downvotes on the post
            reply (bool): true if the post is a reply | false if the post is the original post
            user_name (str): The username of the poster
            url (str): The url where the post can be found
        """
        self.post_id = post_id
        date = date_string 
        self.date = date
        self.title = title
        self.body = body
        self.num_upvotes = num_upvotes
        self.num_downvotes = num_downvotes
        self.reply = reply
        self.user_name = user_name
        self.url = url
    
    def toJSON(self):
        """Get the post in JSON form

        Returns:
            [dict]: The post in JSON form, represented by a Python dictionary
        """
        return {
            "post_id" : self.post_id,
            "date" : self.date,
            "title" : self.title,
            "body" : self.body,
            "num_upvotes" : self.num_upvotes,
            "num_downvotes" : self.num_downvotes,
            "reply" : self.reply,
            "user_name" : self.user_name,
            "url" : self.url
        }
        
    def writeToDatabase(self, collection_name):
        """ Write the post to the database
        """
        collection = database.db[collection_name]
        if collection.count_documents(self.toJSON()) == 0:
            collection.insert_one(self.toJSON())
        