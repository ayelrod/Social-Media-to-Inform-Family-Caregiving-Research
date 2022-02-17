import scrapy
import re
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from als_post import AlsPost

class AlsPastCaregiverSpider(scrapy.Spider):
    """ AlsPastCaregiverSpider is the spider for crawling
        www.alsforums.com
        It can be edited to manage the number
        of pages to scrape.
    """
    name = "als_past_caregivers"
    start_page = 2 # First page to scrape
    end_page = 23 # Last page to scrape
    write_to_database = False # If the posts should be written to the database or not
    collection_name = "AlsPastForums" # Name of the collection in MongoDB
    
    def start_requests(self):
        """ Starts the web scraping for each
            starter url created
            
        Yields:
            dict: The yield output of self.parse
        """
        urls = ["https://www.alsforums.com/community/forums/past-caregivers.60/"]
        for i in range(self.start_page, self.end_page):
            urls.append("https://www.alsforums.com/community/forums/past-caregivers.60/page-" + str(i))
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
        dates = []
        posts = []
        user_names = []
        user_dates = []
        user_num_posts = []
        user_reason_joined = []
        user_diagnosis = []
        user_country = []
        user_state = []
        user_city = []
        
        # Get title of posts
        title = ""
        if len(response.css('div.p-title h1::text')) != 0:
            title = self.clean(response.css('div.p-title h1::text').get())
        
        # Get dates of posts
        for header in response.css('div.message-main header.message-attribution ul.message-attribution-main li.u-concealed a time::attr(data-date-string)').getall():
            date = self.clean(header)
            if date != "":
                date.replace(',', '')
                dates.append(date)
        
        # Get bodies of posts
        for post in response.css("div.bbWrapper"):
            body = self.removeQuote(post)
            body = self.clean(body)
            if body != "":
                posts.append(body)
                
                
        # Get user_name of posters
        for name in response.css("article::attr(data-author)").getall():
            user_names.append(self.clean(name))
            
        # Get user_date_joined and user_num_posts of posters
        for user_stats in response.css("div.message-userExtras"):
            user_stats = user_stats.css("dl")

            counter = 0
            for u in user_stats:
                stat = u.css("dt::text").get()
                stat = self.clean(stat)
                stat = stat.replace(" ", "")
                data = u.css("dd::text").get()
                data = self.clean(data)

                if counter == 0 and stat == "Joined":
                    user_dates.append(data) # maybe do something with a counter to deal with missing values...
                    counter += 1
                    continue
                elif counter == 0 and stat != "Joined":
                    user_dates.append('')
                    counter += 1

                if counter == 1 and stat == "Messages" :
                    user_num_posts.append(int(data))
                    counter += 1
                    continue
                elif counter == 1 and stat != "Messages":
                    user_num_posts.append('')
                    counter += 1    
                
                if counter == 2 and stat == "Reason" :
                    user_reason_joined.append(data)
                    counter += 1
                    continue
                elif counter == 2 and stat != "Reason":
                    user_reason_joined.append('')
                    counter += 1

                if counter == 3 and stat == "Diagnosis" :
                    user_diagnosis.append(data)
                    counter += 1
                    continue
                elif counter == 3 and stat != "Diagnosis":
                    user_diagnosis.append('')
                    counter += 1

                if counter == 4 and stat == "Country" :
                    user_country.append(data)
                    counter += 1
                    continue
                elif counter == 4 and stat != "Country":
                    user_country.append('')
                    counter += 1

                if counter == 5 and stat == "State" :
                    user_state.append(data)
                    counter += 1
                    continue
                elif counter == 5 and stat != "State":
                    user_state.append('')
                    counter += 1     

                if counter == 6 and stat == "City" :
                    user_city.append(data)
                    counter += 1
                    continue
                elif counter == 6 and stat != "City":
                    user_city.append('')
                    counter += 1
            
            if counter <= 6:
                if counter == 4:
                    user_country.append('')
                    user_state.append('')
                    user_city.append('')
                if counter == 5:
                    user_state.append('')
                    user_city.append('')
                if counter == 6:
                    user_city.append('')


        url = response.request.url
        post_id = self.getPostID(url)
        # Yield posts
        if len(dates) == len(posts):
            
            for i in range(len(dates)):
                # If the post is not the first one in the list, it is a reply
                # If the url is not the first page of replies, the posts are all replies
                reply = (i != 0) or (re.match("^(.*?)page=([2-9][0-9]*|1[0-9]+)", response.request.url) != None)
                post = AlsPost(post_id, dates[i], title, posts[i], reply, user_names[i], user_dates[i], user_num_posts[i], user_reason_joined[i], 
                                user_diagnosis[i], user_country[i], user_state[i], user_city[i], response.request.url.rstrip("#ekbottomfooter"))
                if self.write_to_database:
                    post.writeToDatabase(self.collection_name)
                yield post.toJSON()    
        
        # Follow links to reply pages
        if response.css("div.p-title h1::text").get().strip() != 'Past caregivers':
            if response.css("div.pageNav a.pageNav-jump.pageNav-jump--next::attr(href)"):
                a = response.css("div.pageNav a.pageNav-jump.pageNav-jump--next::attr(href)")[0]
                yield response.follow(a, callback=self.parse)
        
        # Follow links to posts   
        if response.css("div.p-title h1::text").get().strip() == 'Past caregivers':
            for a in response.css("div.structItem-title a::attr(href)"):
                    yield response.follow(a, callback=self.parse)
                
    def getPostID(self, url):
        end = 0
        start = 0
        for i in range(len(url)-1, -1, -1):
            if url[i] == '/':
                end = i
                break
        i = end-1 
        while i >= 0:
            if url[i] == '.':
                start = i
                break
            i -= 1
        return url[i+1:end]

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
    
    