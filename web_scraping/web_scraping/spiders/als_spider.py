import scrapy
import re
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from als_post import AlsPost

class AlsSpider(scrapy.Spider):
    """ AlsSpider is the spider for crawling
        www.alsforums.com
        It can be edited to manage the number
        of pages to scrape.
    """
    name = "als"
    start_page = 2 # First page to scrape
    end_page = 2 # Last page to scrape
    
    def start_requests(self):
        """ Starts the web scraping for each
            starter url created
            
        Yields:
            dict: The yield output of self.parse
        """
        urls = ["https://www.alsforums.com/community/forums/current-caregivers.59/"]
        for i in range(self.start_page, self.end_page):
            urls.append("https://www.alsforums.com/community/forums/current-caregivers.59/page-" + str(i))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

            
    def parse(self, response):
        """ Parses the responses we get from
            crawling. Extracts the information from
            a web page and yields it.

        Args:
            response (scrapy.http.response.html.HtmlResponse): The response from links that are followed

        Yields:
            dict: The information that is extracted in JSON form, represented with a Python dict.
        """
        # for post in response.css('div.structItem.structItem'):
        #     yield {
        #         'title': post.css('div.structItem-cell.structItem-cell--main div.structItem-title a::text').get(), 
        #         'username': post.css('div.structItem-cell.structItem-cell--main div.structItem-minor ul.structItem-parts li a::text').get(),
        #         'post_date':  post.css('div.structItem-cell.structItem-cell--main div.structItem-minor ul.structItem-parts li.structItem-startDate a').xpath("//time/@datetime").get(),
        #         'post_text': response.css("div.block-body article.message div.message-inner div.message-cell.message-cell--main div.message-main div.message-content div.message-userContent article.message-body div.bbWrapper::text").get()
        #     }
        #     next_page = post.css('div.structItem-cell.structItem-cell--main div.structItem-title a::attr(href)').get()
        #     if next_page is not None:
        #        yield response.follow(next_page, callback=self.parse)

        if not (self.hasBeenVisited(response.request.url) or self.hasBeenVisited(response.request.url.rstrip("#ekbottomfooter"))):
            dates = []
            posts = []
            user_names = []
            user_dates = []
            user_num_posts = []
            
            # Get title of posts
            title = ""
            if len(response.css('div.p-title h1::text')) != 0:
                title = self.clean(response.css('div.p-title h1::text').get())
            
            # Get dates of posts
            for header in response.css('div.message-main header.message-attribution ul.message-attribution-main li.u-concealed a time::text').getall():
                date = self.clean(header)
                if date != "":
                    date.replace(',', '')
                    dates.append(date)
            
            # Get bodies of posts
            for post in response.css("div.bbWrapper::text"):
                body = self.removeQuote(post)
                body = self.clean(body)
                if body != "":
                    posts.append(body)
                    
                    
            # Get user_name of posters
            for name in response.css('div.message-userDetails h4 a.username').getall():
                user_names.append(self.clean(name))
                
            # Get user_date_joined and user_num_posts of posters
            for user_stats in response.css("div.message-userExtras"):
                user_stats = user_stats.css("dd::text").getall()

                for u in user_stats:
                    u = self.clean(u)
                    u = u.replace(" ", "")

                user_date_joined = user_stats[0].replace(',', '')
                user_num = user_stats[1].replace(',', '')
                user_dates.append(user_date_joined.strip())
                user_num_posts.append(int(user_num))
            
            # Yield posts
            if len(dates) == len(posts):
                print(len(user_dates))
                print(len(user_num_posts))
                print(len(user_names))
                for i in range(len(dates)):
                    # If the post is not the first one in the list, it is a reply
                    # If the url is not the first page of replies, the posts are all replies
                    reply = (i != 0) or (re.match("^(.*?)page=([2-9][0-9]*|1[0-9]+)", response.request.url) != None)
                    post = AlsPost(dates[i], title, posts[i], reply, user_names[i], user_dates[i], user_num_posts[i], response.request.url.rstrip("#ekbottomfooter"))
                    yield post.toJSON()    
            
        #     # Follow links to reply pages
        #     for a in response.css("div.pageNav ul.pageNav-main li a::attr(href)").getall():
        #         yield response.follow(a, callback=self.parse)
        
        # Follow links to posts   
        for a in response.css("div.structItem-title a::attr(href)").getall():
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
    
    def hasBeenVisited(self, url):
        # TODO: Query database to see if the url exists
        return False
        