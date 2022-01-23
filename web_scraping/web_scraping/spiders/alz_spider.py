import scrapy
import re

class AlzSpider(scrapy.Spider):
    name = "alz"
    number_of_pages = 300 # number of pages to scrape
    
    def start_requests(self):
        urls = []
        for i in range(1, self.number_of_pages):
            urls.append("https://www.alzconnected.org/discussion.aspx?g=topics&f=151&page=" + str(i))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        
        if not self.hasBeenVisited(response.request.url):
            dates = []
            posts = []
            
            # Get date of post
            for header in response.css("td.postheader::text").getall():
                date = self.clean(header)
                if date != "":
                    dates.append(date)
            
            # Get body of post 
            for post in response.css("td.message"):
                body = post.get()
                body = self.clean(body)
                if body != "":
                    posts.append(body)
            
            for i in range(len(dates)):
                yield {
                    "date" : dates[i],
                    "body" : posts[i],
                    "url" : response.request.url
                }
        
        for a in response.css("td.alt2 a"):
            yield response.follow(a, callback=self.parse)
            
        for a in response.css("tr.post td a"):
            yield response.follow(a, callback=self.parse)
        
    def clean(self, text):
        text = re.sub('<[^>]+>', ' ', text)
        characters = ['\n', '\r', '\t']
        for character in characters:
            text = text.replace(character, "")
        text = text.lstrip()
        text = text.rstrip()
        return text
    
    def hasBeenVisited(self, url):
        # TODO: Query database to see if the url exists
        return false
        