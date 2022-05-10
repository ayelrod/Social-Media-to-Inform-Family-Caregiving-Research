import scrapy
import re
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from alz_post import AlzPost

class AlzSpider(scrapy.Spider):
    """ AlzSpider is the spider for crawling
        www.alzconnected.org
        It can be edited to manage the number
        of pages to scrape.
    """
    name = "alz"
    start_page = 1 # First page to scrape
    end_page = 300 # Last page to scrape
    write_to_database = False # If the posts should be written to the database or not
    collection_name = "AlzConnected" # Name of the collection in MongoDB

    
    def start_requests(self):
        """ Starts the web scraping for each
            starter url created
            
        Yields:
            dict: The yield output of self.parse
        """
        urls = []
        for i in range(self.start_page, self.end_page):
            urls.append("https://www.alzconnected.org/discussion.aspx?g=topics&f=151&page=" + str(i))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response: scrapy.http.response.html.HtmlResponse):
        """ Parses the responses we get from
            crawling. Extracts the information from
            a web page and yields it.

        Args:
            response (scrapy.http.response.html.HtmlResponse): The response from links that are followed

        Yields:
            dict: The information that is extracted in JSON form, represented with a Python dict.
        """
        dates = []
        posts = []
        user_names = []
        user_dates = []
        user_num_posts = []
        
        # Get title of posts
        title = ""
        if len(response.css("td.header1 div table td")) != 0:
            title = self.clean(response.css("td.header1 div table td").get())
        
        # Get dates of posts
        for header in response.css("td.postheader::text").getall():
            date = self.clean(header)
            if date != "":
                dates.append(date)
        
        # Get bodies of posts
        for post in response.selector.css("td.message"):
            body = self.removeQuote(post)
            body = self.clean(body)
            if body != "":
                posts.append(body)
                
        # Get user_name of posters
        for name in response.css("td b a"):
            user_names.append(self.clean(name.get()))
            
        # Get user_date_joined and user_num_posts of posters
        for user_stats in response.css("td.UserBox").getall():
            user_stats = self.clean(user_stats)
            user_stats = user_stats.replace(" ", "")
            user_date_joined = user_stats[user_stats.find("Joined:") + 7 : user_stats.find("Posts:")]
            user_num = user_stats[user_stats.find("Posts:") + 6 : ]
            user_dates.append(user_date_joined.strip())
            user_num_posts.append(int(user_num))
        
        # Yield posts
        if len(dates) == len(posts):
            for i in range(len(dates)):
                # If the post is not the first one in the list, it is an answer 
                # If the url is not the first page of replies, the posts are all answers
                answer = (i != 0) or (re.match("^(.*?)page=([2-9][0-9]*|1[0-9]+)", response.request.url) != None)
                post = AlzPost(dates[i], title, posts[i], answer, user_names[i], user_dates[i], user_num_posts[i], response.request.url)
                if self.write_to_database:
                    post.writeToDatabase(self.collection_name)
                yield post.toJSON()    
        
        # Follow link to next reply page
        for a in response.css("a.ektopicpagelink"):
            if self.clean(a.get()) == "Next":
                yield response.follow(a, callback=self.parse)
        
        # Follow links to posts   
        for a in response.css("a.post_link::attr(href)"):
            yield response.follow(a, callback=self.parse)
        
    def clean(self, text: str):
        """ Cleans the text passed in.
            Removes the html artifacts and
            some escape characters + whitespace.

        Args:
            text (str): The text to be cleaned

        Returns:
            str: The cleaned up text
        """
        text = re.sub('<[^>]+>', ' ', text)
        characters = ['\n', '\r', '\t', ',']
        for character in characters:
            text = text.replace(character, "")
        text = text.lstrip()
        text = text.rstrip()
        return text
    
    def removeQuote(self, body: scrapy.selector.unified.Selector):
        """ Removes quote blocks from posts.
            Quote blocks in posts are replies
            that include the message being replied
            to in an html class. This is specific
            to the www.alzconnected.org site.

        Args:
            body (): [description]

        Returns:
            [type]: [description]
        """
        quote = body.css("div.quote")

        if quote:
            quote = quote[0].root
            quote.getparent().remove(quote)

        return body.extract()
        