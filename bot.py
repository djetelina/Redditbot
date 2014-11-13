#!/usr/bin/env python

# general imports
import schedule
import time

# bot plugins
import plugins.sidebar as sidebar
import plugins.stalker as stalker

def main():
	# Initiation for getting data
	print "Welcome to /r/scrolls bot."
	username = raw_input("Please enter reddit username: ")
	password = raw_input("Please enter reddit password: ")
	print "Thank you for helping me help you help us all. Let's begin."

	schedule.every(5).minutes.do(lambda: sidebar.streams(username, password))
	schedule.every().hour.do(lambda: sidebar.ladder(username, password))
	schedule.every().hour.do(lambda: stalker.stalk(username, password))

	# on the startup do them both and THEN start counting time
	stalker.stalk(username, password)
	sidebar.streams(username, password)
	print("Waiting 10s for Reddit to update its description, this will only happen once.")
	time.sleep(10)
	sidebar.ladder(username, password)

	while True:
		schedule.run_pending()
		time.sleep(1)

if __name__ == '__main__':
    main()