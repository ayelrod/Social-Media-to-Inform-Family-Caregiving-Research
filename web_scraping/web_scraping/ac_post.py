from datetime import datetime
from post import Post
from urllib.parse import urlparse
from urllib.parse import parse_qs
from mongoDB import MongoDB
import pymongo

# GLOBAL VARIABLE
database = MongoDB() # Create connection to database

class ACPost(Post):
    def __init__(self, post_id: int, date_string: str, title: str, body: str, reply: bool, user_name: str, keywords: list, url: str):
        """Constructor for the ACPost class

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
        self.post_id = post_id
        self.title = title
        self.body = body
        if date_string is None:
            self.date = ""
        else:
            self.date = datetime.strptime(date_string, '%m/%d/%Y %H:%M:%S')
        self.user_name = user_name
        self.reply = reply
        self.keywords = keywords
        self.url = url


        
    def toJSON(self):
        """Get the post in JSON form

        Returns:
            [dict]: The post in JSON form, represented by a Python dictionary
        """
        return {
            "post_id": self.post_id,
            "title" : self.title,
            "body" : self.body,
            "date" : self.date,
            "user_name" : self.user_name,
            "reply" : self.reply,
            "keywords" : self.keywords,
            "url" : self.url
        }
        
    def writeToDatabase(self, collection_name):
        """ Write the post to the database
        """
        collection = database.db[collection_name]
        if collection.count_documents(self.toJSON()) == 0:
            collection.insert_one(self.toJSON())
        