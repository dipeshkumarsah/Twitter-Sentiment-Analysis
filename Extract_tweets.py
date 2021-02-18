import tweepy
from tweepy.auth import OAuthHandler
import csv
import random
import os
import re
import Preprocessing as preprocess
class Extract_tweets:
	# For the authentication required by twitter api
	def authenticate(self):
		# keys and tokens from the Twitter Dev Console
		consumer_key = "QxSDmxsCq1Sf1TsbnyzLAEoJu"
		consumer_secret = "ZDHdBj3CvblX1Y9avzpqvd0QIbAWKdttVQRjd0R2l2HwHBw4gZ"
		access_token = "846700336773423105-pIs0Lzu3aMjfhmXkCUCVDFW1lTIa36S"
		access_token_secret = "wPnL5Bh2J8CzkJwLRn7dGgkde26tVgYkvKV6TwPPS0Kuh"




		# attempt authentication
		try:
			# create OAuthHandler object
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			# set access token and secret
			self.auth.set_access_token(access_token, access_token_secret)
			# create tweepy API object to fetch tweets
			self.api = tweepy.API(self.auth)
			print("successfully authenticated")
		except Exception as e:
			print("Error: Authentication Failed")
			print(e)

	# After authentication, fetch tweets from twitter for specific query
	# Saves fetched tweets to the csv file specified in tweets_not_processed_file_path
	# reurns save file path
	def get_tweets(self,query,count=100,lang="en"):
		#get tweets from tweeter
		fetched_tweets = self.api.search(q=query,count=count,lang=lang)
		path=r"./data"
		#debug
		#to generate different name every time for the file
		self.tweets_not_processed_file_name = "Fetched_tweets_not_processed_"+query+"_"+str(int(random.random()*10000))+".csv"
		self.tweets_not_processed_file_path = os.path.join(path,self.tweets_not_processed_file_name)
		with open(self.tweets_not_processed_file_path,'w',encoding='utf-8',newline='') as csv_file:


			headers = ['tweet_id','tweet_text']
			csv_writer = csv.writer(csv_file)
			csv_writer.writerow(headers)
			i=1
			for tweet in fetched_tweets:
				if(tweet.text):
					row = [str(i),tweet.text]
					csv_writer.writerow(row)
					print(i)
					print(tweet.text)
					i +=1
		return self.tweets_not_processed_file_path
	def get_not_processed_tweets_path(self):
		return self.tweets_not_processed_file_path
	def save_preprocessed_tweets(self):
		with open(self.tweets_not_processed_file_path,'r',encoding='utf-8') as csv_r_file:
			csv_reader = csv.reader(csv_r_file)
			path=r"./data"
			self.tweets_processed_file_path = os.path.join(path,\
													self.tweets_not_processed_file_name[:14]+\
													self.tweets_not_processed_file_name[18:])
			# print(self.tweets_processed_file_path)
			with open(self.tweets_processed_file_path,'w',encoding='utf-8',newline='') as csv_w_file:
				csv_writer = csv.writer(csv_w_file)
				csv_writer.writerow(['tweet_id','processed_tweet'])
				#skip headers
				next(csv_reader)
				for tweet in csv_reader:
					if(len(tweet)==2):
						processed_tweet = preprocess.preprocess_tweets("".join(tweet[1]))
						# print(processed_tweet)
						t = processed_tweet
						t=" ".join(t)
						csv_writer.writerow([tweet[0],t])

		return self.tweets_processed_file_path


	
# test_class = Extract_tweets()
# test_class.authenticate()
# test_class.get_tweets("football")
# test_class.save_preprocessed_tweets()

