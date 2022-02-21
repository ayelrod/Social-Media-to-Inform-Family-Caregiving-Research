# Leveraging Social Media Data to Inform Family Caregiving Research

## About
In recent years, social media has grown exponentially in its use for health-related purposes and, in turn, has become an untapped data source for health research. Social media data offer the potential to observe and generate valuable insight into patients and caregivers’ concerns and priorities, for no or low cost compared to traditional community-engagement methods such as interviews and focus groups. We intend to create a public data repository from family caregiver online discussion forums to enhance the ability to inform and design family caregiving research. The data will be collected by web-scraping posts and replies from two online forums (AlzConnected and ALSForums) and storing it in a database. This will be followed by machine learning and natural language processing to perform sentiment analysis on the text as well as topic modeling. We will also scrape data about the forum users so that future research can explore user-specific research questions. After conducting sentiment analysis, we will use the data to answer various research questions regarding the unmet needs of caregivers, the health of caregivers, and the effects of the pandemic. The data we collect will be adaptable and made public to create opportunities for collaboration in answering future research questions. 

## Install and Run
### Requirements
These packages need to be installed before running the web scrapers:
- scrapy
```
pip install scrapy
```
- pymongo
```
pip install pymongo
```
- dnspython
```
pip install dnspython
```
### Running Scrapers
The scraped data is written to a MonogoDB database as it is scraped. The credentials for this database need to be provided to the program before running. These credentials will be in the form of a MongoDB Connection String. 
Once the connection string is obtained, paste it into a file called '''credentials.txt''' and insert it into the ./web_scrapers/web_scrapers directory.

Once the credentials are inserted, change into the correct directory and run scrapy:
```
cd web_scrapers/web_scrapers
```
Scrapy can be run with either
```
scrapy crawl <spider_name>
```
or
```
scrapy crawl <spider_name> -O <output_file_name>
```
to write the output to a file.

Possible values of <spider_name>
- **alz** for this forum: https://www.alzconnected.org/discussion.aspx?g=topics&f=151
- **als** for this forum: https://www.alsforums.com/community/forums/current-caregivers.59/
- **als_past_caregivers** for this forum: https://www.alsforums.com/community/forums/past-caregivers.60/

***NOTE:*** The scrapers will not run without a valid credentials string in credentials.txt

### Options
There are some variables at the top of each spider that can be configured to change the behavior of the web scrapers. To configure the settings, open up the file containing the spider of interest. These spiders can be found in the ./web_scraping/web_scraping/spiders directory. Once the spider is open, you will see these variable at the top of the class definition:
- **name**: This is the name of the spider, do not change it
- **start_page**: The first page of the forum to scrape
- **end_page**: The last page of the forum to scrape
- **write_to_database**: If True, the data is written to the database. If False, the data is not written to the database.
- **collection_name**: The name of the MongoDB collection to send the data to. *This needs to be configured to match your database information*

There is also a line that should be changed in ./web_scraping/web_scraping/mongoDB.py that should be changed if you are using your own database. The last line should be changed to include your MongoDB database's name.

## Data
### AlzConnected Data
- *post_id*: the post_id is a field that can be used to link posts to eachother. All posts within the same thread have the same post_id. 
- *date*: the date and time of the post (between 11/29/2011 - 02/18/2022)
- *title*: the title of the post
- *body*: the body of the post
- *reply*: True if the post is a reply, False if the post is the original post in the thread
- *user_name*: the username of the post author
- *user_date_joined*: the date the user joined the site (between 08/17/2011 - 02/18/2022)
- *user_num_posts*: the number of posts the user has made on the site
- *url*: the URL to the post

### AlsForums Data
- *post_id*: the post_id is a field that can be used to link posts to eachother. All posts within the same thread have the same post_id. 
- *date*: the date and time of the post (between 05/17/2003 - 02/16/2022)
- *title*: the title of the post
- *body*: the body of the post
- *reply*: True if the post is a reply, False if the post is the original post in the thread
- *user_name*: the username of the post author
- *user_date_joined*: the date the user joined the site (between 04/24/2003 - 02/16/2022)
- *user_num_posts*: the number of posts the user has made on the site
- *user_reason_joined*: the reason the user joined - often abbreviated | CAN BE EMPTY
- *user_diagnosis*: the date the user or user's person was diagnosed | CAN BE EMPTY
- *user_country*: the user's home country | CAN BE EMPTY
- *user_state*: the user's home state | CAN BE EMPTY
- *user_city*: the user's home city | CAN BE EMPTY
- *url*: the URL to the post
