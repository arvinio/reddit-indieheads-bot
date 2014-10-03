"""
DOWNLOAD GOOGLE DATA LIBRARY
https://code.google.com/p/gdata-python-client/downloads/list

INSTALL DATA LIBRARY
unzip gdata.py-yourversionnumber.zip
sudo ./setup.py install

INSTALL DEPENDENCIES GUIDE (unpack in project dir)
https://developers.google.com/api-client-library/python/start/installation

#INSTALL DEPENDENCIES with sudo pip INSTALL
#apiclient, uritemplate, httplib2, oauth2client, urllib3, 
"""

import praw, tweepy, time
import re, urlparse, youtubePlaylist, urllib, urllib2, shutil

access_token = INSERT_ACCESS_TOKEN
access_token_secret = INSERT_ACCESS_TOKEN_SECRET
consumer_key = INSERT_COMSUMER_KEY
consumer_secret = INSERT_CONSUMER_SECRET

open("tweeted.txt", "a")

r = praw.Reddit(user_agent="r/indieheads_Twitter_Bot")
r.login(INSERT_REDDIT_USERNAME, INSERT_REDDIT_PASSWORD)
youtube = youtubePlaylist.get_authenticated_service()

# truncated length of tweet title
def strip_title(title):
	if len(title) < 100:
		return title
	else:
		return title[:96] + "..."

def tweet(text):
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)
		# create instance of tweepy API with arg auth

	api.update_status(text + " #indie #reddit")

def add_to_file(text):
		# called for every tweet
	file = open("tweeted.txt", "a")
	file.write("\r\n" + text)
	file.close()

def found_in_file(text):
	file = open("tweeted.txt", "r")
	lines = file.readlines()

	for row in lines:
		if text.lower() in row:
			file.close()
			return True
	file.close()
	return False

"""Code to get Youtube video ID"""

# Gets youtube video ID from string.
# Example: "[Hey, check out this video.](https://www.youtube.com/watch?v=H_pVkarLMb8)"
# Would return "H_pVkarLMb8"
# Will not return if there are more than one link in a string.
# Courtesy of YT_Bot!

"""
def getVideoID(string):
	#videoID = None
	#yt_count = re.finditer(r'(youtu\.be/)|(youtube\.com/watch)', string)
	#yt_tuple = tuple(yt_count)
	#if len(yt_tuple) > 1:
	#	return None
	if 'youtube.com/watch' in string:
		search = re.search(r'(\?|&(amp;)?)v=([\w-]{11})', string)
        if search:
        	videoID = search.group(3)
	if "youtu.be/" in string:
		search = re.search(r'youtu\.be/([\w-]{11})', string)    
        if search:
            videoID = search.group(1)
	return(videoID)
"""

"""HTTPS POST Request for YouTube OAuth2 refresh token"""
url = "https://accounts.google.com/o/oauth2/token"
values = {
	"refresh_token" : "1/lcmr8ayezu4GwZwjH6xkZRuAcI9rfLAJx2g-OCx-XCQ",
	"client_id" : "211447657248-at4kto7nrn05cu7qblahft8iubjc304i@developer.gserviceaccount.com",
	"client_secret" : "fER23qprwKMm98NthLaYzMPn",
	"grant_type" : "refresh_token"
}

data = urllib.urlencode(values)
req = urllib2.Request(url,data)
response = urllib2.urlopen(req)
myfile = open('file.csv', 'wb')
shutil.copyfileobj(response.fp, myfile)
myfile.close()

# ALTERNATIVE CODE:

# Examples:
#- http://youtu.be/SA2iWivDJiE
#- http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
#- http://www.youtube.com/embed/SA2iWivDJiE
#- http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US


def getVideoID(value):   
	query = urlparse.urlparse(value)
	if query.hostname == 'youtu.be':
		return query.path[1:]
	if query.hostname in ('www.youtube.com', 'youtube.com'):
		if query.path == '/watch':
			p = urlparse.parse_qs(query.query)
			return p['v'][0]
		if query.path[:7] == '/embed/':
			return query.path.split('/')[2]
		if query.path[:3] == '/v/':
			return query.path.split('/')[2]
	# fail?
	return None

def main():
	while True:
		try:
			submissions = r.get_subreddit("indieheads").get_new(limit=80)
			postToReddit(submissions)
			# returns array of last 80 posts
		except Exception, e:
			print "[" + time.strftime("%H:%M:%S") + "] ---Oops! Failed to get posts---"
			submission = []
			time.sleep(301)
		print
		print "[" + time.strftime("%H:%M:%S") + "] ---Now sleeping for 5 min. Then fetching new posts.---"
		print
		time.sleep(301)

def postToReddit(submissions):
	for submission in submissions:
		if "fresh" in submission.title.lower():
				#converts submission titles to lowercase then checks for keyword "fresh"
			if not vars(submission)["is_self"]:
				if not found_in_file(str(submission.short_link)): 
					# if link not found in file, proceed
					print "Posting: " + strip_title(submission.title) + " (" + str(submission.short_link) + ")"
					tweetPost(submission)

def tweetPost(submission):
	for tries in range(0, 3):
		try:
			tweet(strip_title(submission.title) + " (" + str(submission.short_link) + ")")	
			commentReddit(submission)
			break
		except Exception, e:
			print
			if '187' in str(e):
				break
			print e
			print "[" + time.strftime("%H:%M:%S") + "] ---Oops! Failed to tweet (try %s/3). Trying again in 5 min---" %(tries+1)
			print
			time.sleep(301)

def commentReddit(submission):
	for tries in range(0, 3):
		
		try:
			submission.add_comment("Hi! I just tweeted this. Check it out [@r_indieheads](https://twitter.com/r_indieheads) :)\r\n\r\nAll YouTube links are added to [**this**](https://www.youtube.com/playlist?list=PLBAONYajiBCUoZgLRWRCDLKPN-MAN_Wdb) playlist!\r\n\r\n=================\r\n\r\n\r\n[^^Source ^^Code](https://github.com/Barvin/reddit-indieheads-bot) ^^| [^^Donate!](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=7EV6XMH7DU76E)")
			break
		except Exception, e:
			print e
			print "[" + time.strftime("%H:%M:%S") + "] ---Oops! RateLimitExceeded (try %s/3). Trying again in 5 min---" %(tries+1)
			print
			time.sleep(301)
		addToPlaylist(submission)

def addToPlaylist(submission):
	for tries in range(0, 8):
	
		if "youtube.com/watch" or "youtu.be/" in str(submission.url):
			print "submission url: ", str(submission.url)
			print "video ID: ", getVideoID(str(submission.url))
			if not getVideoID(str(submission.url)) is None:
				try:
					youtubePlaylist.add_video_to_playlist(youtube,getVideoID(str(submission.url)),"PLBAONYajiBCUoZgLRWRCDLKPN-MAN_Wdb")
					break
				except Exception, e:
					print "\r\n", str(e), "\r\n"
					if 'BadStatusLine' or "HTTPError" in str(e):
						break
					print e
					print "[" + time.strftime("%H:%M:%S") + "] ---Oops! Couldn't add to YouTube Playlist. (try %s/3). Trying again in 10 min---" %(tries+1)
					print
					time.sleep(180)
	add_to_file(str(submission.short_link))

main()
