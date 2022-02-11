from abc import ABC, abstractmethod

class Post(ABC):
    """ Post is an abstract class to 
        represent a post in the sites
        we scrape
    """
    
    @abstractmethod
    def toJSON(self):
        pass
      
    @abstractmethod  
    def writeToDatabase(self):
        pass
    