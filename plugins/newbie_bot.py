#Newbie Bot created by pizzamanzoo
import time
import praw 
import os

def reply(username, password, already_done):
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
        
    #Look at all submissions from all time
    for submission in subreddit.get_new(limit=None):
        flag = 1
        #makes sure submission isn't done twice
        if submission.id in already_done:
            flag = 0
        print "Looking through submissions"

        #Gets all comments from the submission
        all_comments = submission.comments
        if flag == 1:
            #looks at each comment
            for comment in all_comments:
                op_text = comment.body
                print "looing at text"
                has_praw = any(string in op_text for string in prawWords)
                print "sees if words are in post"
                #If the words are there, post reply
                if submission.id not in already_done and has_praw:
                    #post reply
                    print "Posting reply"
                    submission.add_comment(post_text)
                    #Add this post to the already done list
                    already_done.append(submission.id)
            print "End of reply loop"
    print "End of search"
