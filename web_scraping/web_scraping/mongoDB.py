import pymongo
import json

class MongoDB():
    def __init__(self):
        self.db = self.get_database()
    
        
    def get_database(self):
        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        credentials_file = open("credentials.txt", "r")
        CONNECTION_STRING = credentials_file.read()

        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        client = pymongo.MongoClient(CONNECTION_STRING)

        # Create the database for our example (we will use the same database throughout the tutorial
        return client['SocialMediaCaregivingResearch']