import praw
from psaw import PushshiftAPI
import datetime
from reddit_post import RedditPost
from praw.models import MoreComments

def scrape_subreddit(subreddit_name):
    gen = api.search_submissions(
        # before=int(datetime.datetime(2018, 4, 20).timestamp()), 
        # after=int(datetime.datetime(2018, 4, 20).timestamp()),
        subreddit=subreddit_name, 
        # limit=10,
        )
    results = list(gen)
    print(len(results))
    i = 0
    for submission in results:
        # uncomment this to post
        # print_single_submission_info(submission)
        print(i)
        i = i + 1

def print_single_submission_info(submission):
    post = RedditPost(submission.id, datetime.datetime.fromtimestamp(submission.created), 
        submission.title, submission.selftext, submission.ups, submission.downs, False, 
        str(submission.author), submission.url)
    post.toJSON()
    post.writeToDatabase(collection)

    for comment in submission.comments.list():
        if isinstance(comment, MoreComments):
            continue
        print_single_comment_info(comment, submission.title, submission.url)

def print_single_comment_info(submission, title, url):
    post = RedditPost(submission.id, datetime.datetime.fromtimestamp(submission.created), 
        title, submission.body, submission.ups, submission.downs, True, 
        str(submission.author), url)
    post.toJSON()
    post.writeToDatabase(collection)


reddit = praw.Reddit()
api = PushshiftAPI(reddit)
# collection = "Reddit-CaregiverSupport"
# scrape_subreddit("CaregiverSupport")
# collection = "Reddit-Alzheimers"
# scrape_subreddit("Alzheimers")
# collection = "Reddit-Caregivers"
# scrape_subreddit("caregivers")
collection = "Reddit-Caregiving"
scrape_subreddit("caregiving")
