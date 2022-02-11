import pymongo
import json

class MongoDB():
    def __init__(self):
        self.db = self.get_database()
        
    def get_database(self):
        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        CONNECTION_STRING = "mongodb+srv://cluster0.jtuyt.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"

        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        client = pymongo.MongoClient(CONNECTION_STRING)

        # Create the database for our example (we will use the same database throughout the tutorial
        return client['SocialMediaCaregivingResearch']