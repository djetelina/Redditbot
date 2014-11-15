#!/usr/bin/env python

import schedule
import time
import praw
import urllib2
import sys
import json
import datetime
import os

reddit = None
subreddit_name = "scrolls"

sentinel = "[~s~](/s)"
username = ""
password = ""

def login(username, password):

    global reddit

    reddit = praw.Reddit(user_agent='/r/scrolls sidebar updater [praw]')
    reddit.login(username, password)

def get_description():

    global reddit
    global subreddit_name

    return reddit.get_subreddit(subreddit_name).get_settings()['description']

def update_description(new_description):

    global reddit
    global subreddit_name

    print(time.strftime('%H:%M:%S Sidebar update complete', time.localtime()))

    reddit.get_subreddit(subreddit_name).update_settings(description=new_description)


def streams(username, password):
    script_dir = os.path.dirname(__file__)
    rel_path = "logs/streamers.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    log = open(abs_file_path, "a")

    print(time.strftime('%H:%M:%S Initiating live streams update', time.localtime()))

    # between 1. and 2. sentinel
    try:
        login(username, password)
        old_description = get_description()

        parts = old_description.split(sentinel)

        # Waypoints release for fun
        # countdown = datetime.datetime(2014, 9, 23) - datetime.datetime.now()
        # release = str((countdown.seconds/3600)+16) + " hours"
        # waypoints = "\n\n**Waypoints**\n\n* Get it in your local Scrolls client NOW!\n\n* New Scrolls: [Gallery](http://imgur.com/a/oNa9D)\n\n* Changelog: [self post](http://www.reddit.com/r/Scrolls/comments/2h887x/waypoints_and_black_market_complete_changelog/)\n\n"
        
        f = urllib2.urlopen("https://api.twitch.tv/kraken/streams?game=Scrolls&limit=10")
        twitch_api = f.read()
        f.close()
        res = json.loads(twitch_api)

        if len(res["streams"]) > 0:
            # streams = waypoints + "\n\n**Live streams**\n\n"
            streams = "\n\n**Live streams**\n\n"
            print("Streams LIVE:")
            for stream in res["streams"]:
                viewers = stream["viewers"]
                channel = stream["channel"]
                name = channel["display_name"]
                url  = channel["url"]
                streams += " * [%s (%s)](%s)\n" % (name,viewers,url)
                print("%s with %s viewers" % (name,viewers))
                log.write("{\"time\":\"" + (time.strftime('%d.%m.%Y %H:%M:%S', time.localtime())) + "\",\"streamer\":\"" + '%s' % (name) + "\"},\n")
        else:
            # streams = waypoints + "\n\n**Live streams**\n\n"
            streams = "\n\n**Live streams**\n\nNo streams online."

        parts[1] = streams

        # -------------------------------------------------------

        new_description = sentinel.join(parts)

        update_description(new_description)
    except Exception as e:
        print("Error loading streams: " + str(e))




def ladder(username, password):
    # between 3. and 4. sentinel
    print(time.strftime('%H:%M:%S Initiating ladder update', time.localtime()))
    try:
        login(username, password)
        old_description = get_description()

        parts = old_description.split(sentinel)

    # -------------------------------------------------------
    # edit part 3

    # a.scrollsguide.com doesn't like urllib, so apparently we're Google Chrome!
        request = urllib2.Request("http://a.scrollsguide.com/ranking?limit=10&fields=name,rating,rank")
        request.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36")
    
        f = urllib2.urlopen(request)
        sg_api = f.read()
        f.close()

        res = json.loads(sg_api)
        top10 = ""

        if res['msg'] == 'success':
            i = 0
            for player in res['data']:
                i += 1
                top10 = "%s %d. %s (%d) \n" % (top10, i, player['name'], player['rating'])

            top10 = '\n\n**Ladder (top 10)**\n\n' + top10 + '\n\n[More at SG/ranking](http://scrollsguide.com/ranking)\n\n' + "[Last updated at %s](/smallText)" % time.strftime('%H:%M:%S UTC', time.gmtime())

        parts[3] = top10

        # -------------------------------------------------------

        new_description = sentinel.join(parts)

        update_description(new_description)
    except Exception as e:
        print("Error loading ladder: " + str(e))




def sidebar(username, password):


    schedule.every(5).minutes.do(streams(username, password))
    schedule.every().hour.do(ladder(username, password))

    streams(username, password)
    print("--- Waiting 30s for Reddit to update its description")
    time.sleep(30)
    ladder(username, password)

    while True:
        schedule.run_pending()
        time.sleep(1)




if __name__ == '__main__':
    sidebar()
