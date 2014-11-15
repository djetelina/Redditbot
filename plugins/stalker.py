#!/usr/bin/env python

# -*- coding: utf-8 -*-

#Config Here:
subreddit_name = "Scrolls"
subreddit_id = "t5_2scq0"
page = "stalker"
devs = ["MansOlson","carnalizer","BomuBoi","jonkagstrom","poipoichen", "SeeMeScrollin", "Atmaz", "Marc_IRL", "jeb_", "aronnie", "krisjelbring"]
newcontent = ""

import json
import datetime
import urllib2
import time
import praw
import schedule
import sys
from ago import human
 
posts = []
reddit = None

def login(username, password):

	global reddit

	reddit = praw.Reddit(user_agent='Mojang stalker for /r/scrolls [praw]')
	reddit.login(username, password)
 
def stalk(username, password):
	print(time.strftime('%H:%M:%S Initiating stalking', time.localtime()))
	try:
		login(username, password)
		for dev in devs:
			time.sleep(10)
			hdr = { 'User-Agent' : 'Mojang stalker bot for /r/scrolls' }
			req = urllib2.Request("http://www.reddit.com/user/%s/comments.json?limit=10"%dev, headers=hdr)
			h = urllib2.urlopen(req)
			d = json.loads(h.read())
			for p in d["data"]["children"]:
				# Filter only a specific subreddit
				if p["data"]["subreddit_id"] == subreddit_id:
					posts.append(p)
		 
		# Sort by the time the post was created
		posts.sort(key=lambda p: p["data"]["created"],reverse=True)
		
		newcontent = ""
		for post in posts[0:20]:
			timestamp = human(datetime.datetime.fromtimestamp(post["data"]["created"]) - datetime.timedelta(hours=8))
			thread_id = post["data"]["link_id"][3:]
			comment_id = post["data"]["id"]
			url = "http://www.reddit.com/r/%s/comments/%s//%s?context=3" % (subreddit_name,thread_id,comment_id)
			newcontent += "[](/mojang) /u/%s (%s) [%s](%s) by /u/%s \n\n>%s\n\n****\n\n" % (post["data"]["author"], timestamp, post["data"]["link_title"], url, post["data"]["link_author"], post["data"]["body"].replace("\n","\n> "))
		del posts[:]
		reddit.edit_wiki_page(subreddit=subreddit_name, page=page, content=newcontent, reason='')
		print(time.strftime('%H:%M:%S Stalking complete', time.localtime()))
	except Exception as e:
		print("Error stalking: " + str(e))

def stalker(username, password):

	schedule.every().hour.do(stalk(username, password))

	stalk(username, password)

	while True:
		schedule.run_pending()
		time.sleep(1)

if __name__ == '__main__':
	stalker()