#!/usr/bin/env python

# general imports
import schedule
import time

# bot plugins
import plugins.sidebar as sidebar
import plugins.stalker as stalker
import plugins.spritesheeter as spritesheeter

def main():

	# Choose plugins to run
	print "\n\nWelcome to /r/scrolls bot. Choose your weapon:\n"
	print "=============================================="
	print "1: Sidebar updates and mojangsta stalking."
	print "2: create emoticon spritesheet."
	print "==============================================\n"
	whattodo = raw_input("What will it be?\n")

	if whattodo == "1":
		print "You chose to run script that's updating sidebar and stalks mojangstas."
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

	elif whattodo == "2":
		print "You chose to create emoticon spritesheet"
		spritesheeter.emoti()

	else:
		print "Let's try that again."
		main()

if __name__ == '__main__':
    main()