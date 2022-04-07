from calendar import c
import scrapy
import re
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ac_post import ACPost

class ACSpider(scrapy.Spider):
    """ ACSpider is the spider for crawling
        www.agingcare.com
        It can be edited to manage the number
        of pages to scrape.
    """
    name = "ac"
    start_page = 2 # First page to scrape
    end_page = 3881 # Last page to scrape, 3,879 total
    write_to_database = True # If the posts should be written to the database or not
    collection_name = "AgingCare-Questions" # Name of the collection in MongoDB

    def start_requests(self):
        urls = ["https://www.agingcare.com/caregiver-forum/questions"]
        for i in range(self.start_page, self.end_page):
            urls.append("https://www.agingcare.com/caregiver-forum/questions?page=" + str(i))
                        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # get post titles:
        #title = self.clean(response.css('head meta::attr(content)')[7].get())
        title = response.css('div.question-page section a h1::text').get()

        # get dates of posts:
        dates = []
        dates.append(response.css('div.question-page meta::attr(content)').get())       # get original post date
        replies = response.css('div.comments-page time::attr(datetime)').getall()       # get reply dates
        for r in replies:
            dates.append(r)

        # Get bodies of posts:
        posts = []   
        body = response.css('p').get() # gets original post
        body = self.clean(body)
        posts.append(body)

        replies = response.css('div.comments-page div.commentheader div.pad-btm-m div.text').getall()  # gets replies
        for reply in replies:
            reply = self.clean(reply)
            if reply != "":
                posts.append(reply)

        # Get user_names of posters: 
        user_names = []
        for name in response.css('span.text.small.blue-link.semi-bold::text').getall():
            user_names.append(name)
        
        # get post keywords:
        post_keywords = []
        original = response.css('head meta::attr(content)')[5].get()
        post_keywords.append(original.split(','))
        i = 1
        while i < len(user_names):
            post_keywords.append([])        # put empty string for reply keywords 
            i += 1

        # Yield Posts
        url = response.request.url
        post_id = url[len(url)-10: len(url)-4]
        if len(dates) == len(posts):
            for i in range(len(dates)):
                # If the post is not the first one in the list, it is an reply
                # If the url is not the first page of replies, the posts are all replies
                reply = (i != 0) or (re.match("^(.*?)page=([2-9][0-9]*|1[0-9]+)", response.request.url) != None)
                if posts[i] == 'Assisted Living':
                    continue
                post = ACPost(post_id,dates[i], title, posts[i], reply, user_names[i], post_keywords[i], url)
                if self.write_to_database:
                    post.writeToDatabase(self.collection_name)
                yield post.toJSON()

        # Follow links to reply pages
        if response.css('div.threadBlock div.comments-page a.text::attr(href)').get() is not None:  # follow "See All Pages Link" if it exists
            a = response.css('div.threadBlock div.comments-page a.text::attr(href)')        
            yield response.follow(a, callback=self.parse)

        # Follow links to post
        allLinks = response.css('div.forumList div.forumEntry a::attr(href)').getall()
        for link in allLinks:
            if link.startswith('/questions/'):
                yield response.follow(link, callback=self.parse)
        
        for a in response.css('div.pagination-container a::attr(href)'):
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
