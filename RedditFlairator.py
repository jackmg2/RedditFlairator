import praw
import os
import webbrowser
import random
import string
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Main script
def main():
    CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    USERNAME = os.getenv('REDDIT_USERNAME')
    USER_PASSWORD = os.getenv('REDDIT_PASSWORD')

    # Initialize Reddit instance with the access token
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        username=USERNAME,
        password=USER_PASSWORD,
        user_agent="flairator/1.0"
    )

    print(reddit.user.me())

    # Specify the subreddit
    subreddit_name = os.getenv('SUBREDDIT_NAME')
    subreddit = reddit.subreddit(subreddit_name)

    # Specify the flair text and CSS class
    flair_text = os.getenv('FLAIR_TEXT')
    flair_css_class = os.getenv('FLAIR_CSS')

    def apply_flair_and_approve(username_list):
        for username in username_list:
            try:
                # Get the Redditor object
                user = reddit.redditor(username.strip())
                
                # Apply flair
                subreddit.flair.set(user, text=flair_text, css_class=flair_css_class)
                print(f"Applied flair to user: {username}")
                
                # Approve the user
                subreddit.contributor.add(user)
                print(f"Approved user: {username}")
            
            except praw.exceptions.RedditAPIException as e:
                print(f"Error processing user {username}: {str(e)}")

    # Get the list of usernames from user input
    user_input = input("Enter a comma-separated list of usernames: ")
    usernames = user_input.split(',')
    
    # Apply flair and approve users
    apply_flair_and_approve(usernames)
    
    print("Script execution completed.")

if __name__ == "__main__":
    main()