import praw
import config
import time
import os
import requests
import random


def bot_login():
	print "Logging in..."
	r =	praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = "Reddit song bot")
	print "Logged in!"

	return r

def run_bot(r, comments_replied_to):
	print "Obtaining 50 comments..."

	for comment in r.subreddit('test').comments(limit=50):
		if "!song" in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me():
			print "String with \"!song\" found in comment " + comment.id

			comment_reply = "You requested a new song! Here it is:\n\n"

			songid = random.randint(1,config.maxSong)

			songid = str(songid)

			song = requests.get(config.APISong+songid+config.accessToken).json()['response']['song']['full_title']


			#song = requests.get('https://api.genius.com/songs/2471960?access_token=CXyFeSBw2lAdG41xkuU3LS6a_nwyxwwCz2dCkUohw-rw0C49x2HqP__6_4is5RPx').json()['response']['song']['full_title']

			comment_reply += ">" + song

			comment_reply += "\n\nThis song request fulfilled from [api.genius.com](http://api.genius.com/)."

			comment.reply(comment_reply)
			print "Replied to comment " + comment.id

			comments_replied_to.append(comment.id)

			with open ("comments_replied_to.txt", "a") as f:
				f.write(comment.id + "\n")

	print "Sleeping for 10 seconds..."
	#Sleep for 10 seconds...
	time.sleep(10)

def get_saved_comments():
	if not os.path.isfile("comments_replied_to.txt"):
		comments_replied_to = []
	else:
		with open("comments_replied_to.txt", "r") as f:
			comments_replied_to = f.read()
			comments_replied_to = comments_replied_to.split("\n")
			comments_replied_to = filter(None, comments_replied_to)

	return comments_replied_to

r = bot_login()
comments_replied_to = get_saved_comments()
print comments_replied_to

while True:
	run_bot(r, comments_replied_to)