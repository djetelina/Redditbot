#Newbie Bot created by pizzamanzoo
import time
import praw 
import os

def reply(username, password, comments_done, posts_done):
    #Set the message for reddit
    r = praw.Reddit("Newbie Bot for r/scrolls by /u/pizzamanzoo v 1.0")
    
    #login with u/p combo
    r.login(username, password)
    #Initialize list of posts

    #Words the bot will look for
    prawWords = ['/u/ScrollsBot'] #add phrases or words here

    script_dir = os.path.dirname(__file__)
    rel_path = "scrolls_bot_reply.md"
    abs_file_path = os.path.join(script_dir, rel_path)

    #Opens the post file and reads it into a var
    post_file = open(abs_file_path, "r+")
    post_text = post_file.read(2326) #replace with byte count from file

    print(time.strftime("%H:%M:%S Inititing Newbie Bot")) 

    #Set the subreddit name here
    subreddit = r.get_subreddit('scrolls')
    all_comments = subreddit.get_comments()
    flag = 1

    if flag == 1:
        for comment in all_comments:  
            if comment.id in comments_done:
                flag = 0
                break
            com_text = comment.body
            has_praw = any(string in com_text for string in prawWords)
            if has_praw: 
                if comment.submission.id not in posts_done:
                    comment.submission.add_comment(post_text)
                    posts_done.append(comment.submission.id)
            comments_done.append(comment.id)
