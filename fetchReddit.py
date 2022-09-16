import re
import os
from os.path import join, dirname
from dotenv import load_dotenv
import praw

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

CLIENT_ID = os.environ.get("CLIENT_ID")
SECRET = os.environ.get("SECRET")
USER_AGENT = os.environ.get("USER_AGENT")

# Read-only instance
reddit_read_only = praw.Reddit(client_id=CLIENT_ID,
                               client_secret=SECRET,
                               user_agent=USER_AGENT)

subreddit = reddit_read_only.subreddit("vtubers")

posts = subreddit.top(limit=250_000, time_filter="year")

posts_dict = {"Title": [], "Post Text": []}

with open('reddits/lastYear.txt', 'w') as file:
    for post in posts:
        file.write(re.sub(r'http\S+', '', post.title.replace('\n', ' ') + ' ' + post.selftext).replace('\n', ' '))
        file.write('\n')
