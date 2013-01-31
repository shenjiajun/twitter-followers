import json
import urllib2
import csv
import oauth2 as oauth
import httplib
import codecs
import time
import sys
from sys import stdout

##### settings #####

twitter_user = 'twitter_user'
oauth_req_key = 'oauth_req_key'
oauth_req_sec = 'oauth_req_sec'
oauth_consumer_key = 'oauth_consumer_key'
oauth_consumer_sec = 'oauth_consumer_sec'

####################


url_followers = "https://api.twitter.com/1/followers/ids.json?cursor=-1&screen_name=" + twitter_user
url_lookups = "https://api.twitter.com/1/users/lookup.json?user_id=%USER_IDS%&include_entities=true"
#test = "https://graph.facebook.com/19292868552"

def main():
	if(len(sys.argv) < 3):
		print "usage: python followers.py start_number end_number"
		print "for example, to export first 200 followers: python followers.py 1 200"
		print "to export all, python followers.py 1 99999999..."
		exit()
	json_followers = json.loads(oauth_req(url_followers))
	follower_ids = json_followers["ids"]
	follower_ids.sort()
	follower_ids = follower_ids[int(sys.argv[1])-1 : int(sys.argv[2])]

	print str(len(follower_ids))+' followers are being exported to output.csv file'
	fd = codecs.open('output.csv','w','utf-8')
	fd.write(u'\ufeff')
	fd.close()
	stdout.write("Exporting")
	
	batch = 100 # max number of users to look up in a single API call which is limited to 100 by twitter
	while (len(follower_ids) > batch - 1): 
		comma_delimited = ','.join(str(i) for i in follower_ids[0 : batch]) #full batch number as python excludes higher index
		push_to_file(comma_delimited)
		follower_ids = follower_ids[batch:]
		stdout.write(".")
		time.sleep( 1 )
	
	if(len(follower_ids) > 0):
		comma_delimited = ','.join(str(i) for i in follower_ids[0:])
		push_to_file(comma_delimited)
		stdout.write(".")
	stdout.write("\n")
	print("Done.")


def oauth_req(url, key=oauth_req_key, secret=oauth_req_sec, http_method="GET", post_body=None,
        http_headers=None):
    consumer = oauth.Consumer(key=oauth_consumer_key, secret=oauth_consumer_sec)
    token = oauth.Token(key=key, secret=secret)
    client = oauth.Client(consumer, token)
    resp, content = client.request(
		url,
        method=http_method
    )
    return content

# append commma separated followers to CSV file
def push_to_file(ids):
	#print (url_lookups.replace("%USER_IDS%", ids))
	#print '---'
	#return
	
	try:
		json_lookups = json.loads(oauth_req(url_lookups.replace("%USER_IDS%", ids)), encoding="utf-8")
	except Exception, err:
		print url_lookups.replace("%USER_IDS%", ids)
		raise
	#append
	fd = codecs.open('output.csv','a','utf-8')
	for i in range(0, len(json_lookups)):
		#fields
		name = json_lookups[i]["name"]
		if name is None:
			name = 'None'
		screen_name = json_lookups[i]["screen_name"]
		followers_count = json_lookups[i]["followers_count"]
		if followers_count is None:
			followers_count = 0
		description = json_lookups[i]["description"]
		if description is None:
			description = 'None'
		location = json_lookups[i]["location"]
		if location is None:
			location = 'None'
		lang = json_lookups[i]["lang"]
		if lang is None:
			lang = 'None'
		followers_count_category = ''
		if followers_count < 51:
			followers_count_category = '0-50'
		elif followers_count < 201:
			followers_count_category = '51-200'
		elif followers_count < 501:
			followers_count_category = '201-500'
		elif followers_count < 1001:
			followers_count_category = '501-1000'
		elif followers_count < 10001:
			followers_count_category = '1001-10000'
		else:
			followers_count_category = '>10000'
		fd.write(name.replace(',',' ') + ',' + screen_name + ',' + str(followers_count_category) + ',' + description.replace('\r\n',' ').replace('\r',' ').replace('\n',' ').replace(',',' ') + ',' + location.replace(',',' ') + ',' + lang)
		fd.write('\n')
	fd.close()
	
if __name__ == "__main__":
    main()
	
