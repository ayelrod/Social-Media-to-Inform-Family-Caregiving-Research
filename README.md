# Leveraging Social Media Data to Inform Family Caregiving Research

## About
  In recent years, social media has grown exponentially in its use for health-related purposes and, in turn, has become an untapped data source for health research. Social media data offer the potential to observe and generate valuable insight into patients and caregivers’ concerns and priorities, for no or low cost compared to traditional community-engagement methods such as interviews and focus groups. We intend to create a public data repository from family caregiver online discussion forums to enhance the ability to inform and design family caregiving research. The data will be collected by web-scraping posts and replies from several online forums (AlzConnected, ALSForums, AgingCare, Reddit) and storing it in a database. This will be followed by machine learning and natural language processing to perform sentiment analysis on the text as well as topic modeling. We will also scrape data about the forum users so that future research can explore user-specific research questions. After conducting sentiment analysis, we will use the data to answer various research questions regarding the unmet needs of caregivers, the health of caregivers, and the effects of the pandemic. The data we collect will be adaptable and made public to create opportunities for collaboration in answering future research questions. 

## Install and Run Web Scrapers
### Requirements
These packages need to be installed before running the web scrapers:
- Scrapy
- pymongo
- dnspython
```
pip install scrapy
pip install dnspython
pip install pymongo
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
- **ac** for this forum: https://www.agingcare.com/caregiver-forum/questions
- **ac-discussion** for this forum: https://www.agingcare.com/caregiver-forum/discussions

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
- *support_type*: Some posts may have a support_type field. These were added through manual labeling and designate the support type that the post is requesting

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

### AgingCare (Questions and Discussions Forum) Data
- *post_id*: the post_id is a field that can be used to link posts to eachother. All posts within the same thread have the same post_id. 
- *title*: the title of the post
- *body*: the body of the post
- *date*: the date and time of the post (between 10/18/2007 - 04/06/2022)
- *user_name*: the username of the post author
- *reply*: True if the post is a reply, False if the post is the original post in the thread
- *keywords*: the keywords selected for main post by user
- *url*: the URL to the post

### Reddit Data (r/Alzheimers, r/CaregiverSupport, r/Caregivers, r/Caregiving)
- *post_id*: The ID of the post
- *date*: The date and time of the post
- *title*: The title of the post
- *body*: The body of the post
- *num_upvotes*: The number of upvotes the post received
- *num_downvotes*: The number of downvotes the post received
- *reply*: True if the post is a reply, False if the post is the original post in the thread
- *user_name*: the username of the post author
- *url*: the URL to the post

## NLP
### Pre-Processing and Tokenization
In order to perform NLP on the text data, we first need to clean it and tokenize it. First, we split the text into a list of words. Punctuations and stopwords are then removed and we are left with our words of interest. The words are then lemmatized by stripping words down to their base. An example of this would be stripping the word "being" to "be" to get its most basic form. This leaves us with our tokens in the form of a list of words, which are used to represent each post. 

In Sentiment Analysis, further processing is needed to turn these lists of words into features. The first step in doing this is to find the frequency of each word in all the posts of interest combined. Then we take the 2000 most frequent words and those become our features. A post is then represented by a Python dictionary which maps each feature to a boolean value of wether or not that feature is contained in the document.    
  
  
### Topic Modeling
Topic Modeling is done using a process called LDA (Latent Dirichlet Allocation), provided in the gensim and pyLDAvis libraries. LDA outputs a specified number of topics with words that are most likely to belong to those topics.  
  
  
### Sentiment Analysis
Sentiment Analysis was done using NLTK's SentimentIntensityAnalyzer and NaiveBayesClassifier. The first step was to mark each post as positive or negative. We did this by using the SentimentIntensityAnalyzer to get the polarity of text, which is a value from [-1, 1] with -1 being the most negative and 1 being the most positive. Neutral posts (value of 0) are marked as Negative during the sentiment analysis. We also got the subjectivity of each post, which is a value from [0, 1] with 0 being the most objective and 1 being the most subjective. Labeling posts as positive or negative is done using VADER (Valence Aware Dictionary for Sentiment Reasoning). This model takes into account the general sentiment of a post (polarity) and the intensity of emotion. The model can also understand context at a basic level when analyzing words.

Once that was done, we could use NLTK's Naive Bayes Classifier to get a better sense of which words are linked to negative and positive sentiments. This output shows us how much more likely a word is to be associated with either a negative or positive sentiment.

### Emotion Analysis
Emotion Analysis was done using the NRCLex library. This library mainly applies emotion scores for 10 different emotions by looking at the words in the text and finding ones commonly associated with an emotion. These emotions are:
- fear
- anger
- anticipation
- trust
- surprise
- positive
- negative
- sadness
- disgust
- joy
