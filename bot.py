#!/usr/bin/env python

# general imports
import schedule
import time

# bot plugins
import plugins.sidebar as sidebar
import plugins.stalker as stalker
import plugins.newbie_bot as newbie_bot
import plugins.spritesheeter as spritesheeter

def main():
	
	posts_done = []
	comments_done = []
	# Choose plugins to run
	print "\nWelcome to /r/scrolls bot. Choose your weapon:\n"
	print "=============================================="
	print "1: Sidebar updates, mojangsta stalking, and newbie bot."
	print "2: Create emoticon spritesheet."
	print "==============================================\n"
	whattodo = raw_input("What will it be?\n")

	if whattodo == "1":
		print "You chose to run script that's updating sidebar, stalks mojangstas, and replies to newbies."
		username = raw_input("Please enter reddit username: ")
		password = raw_input("Please enter reddit password: ")
		print "Thank you for helping me help you help us all. Let's begin."

		schedule.every(5).minutes.do(lambda: sidebar.streams(username, password))
		schedule.every().hour.do(lambda: sidebar.ladder(username, password))
		schedule.every().hour.do(lambda: stalker.stalk(username, password))
		schedule.every(10).minutes.do(lambda: newbie_bot.reply(username, password, comments_done, posts_done))

		# on the startup do them both and THEN start counting time
		stalker.stalk(username, password)
		sidebar.streams(username, password)
		print("Waiting 10s for Reddit to update its description, this will only happen once.")
		time.sleep(10)
		sidebar.ladder(username, password)
		newbie_bot.reply(username, password, comments_done, posts_done)


		while True:
			schedule.run_pending()
			time.sleep(1)

	elif whattodo == "2":
		print "You chose to create emoticon spritesheet, let's begin."
		spritesheeter.emoti()
		main()

	else:
		print "Let's try that again."
		main()

if __name__ == '__main__':
	main()
