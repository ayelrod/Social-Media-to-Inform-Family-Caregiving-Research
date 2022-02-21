# Leveraging Social Media Data to Inform Family Caregiving Research

## Install and Run
### Requirements
These packages need to be installed in order to run the web scrapers:
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

### AlsForums
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
