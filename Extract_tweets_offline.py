import csv
import random
import os
import re
import Preprocessing as preprocess
class Extract_tweets_offline:
	def get_tweets(self,query,count=100,lang="en"):
		#get tweets from offline dataset
		extract_file_name = query
		path=r".\dataset"
		extract_file_path = os.path.join(path,extract_file_name)
		with open(extract_file_path,'r',encoding='utf-8') as extract_file:
			tweets=[]
			csv_reader = csv.reader(extract_file)
			for line in csv_reader:
				tweets.append(line[1])
		fetched_tweets = tweets
		path=r".\data"
		#debug
		#to generate different name every time for the file
		self.tweets_not_processed_file_name = "Fetched_tweets_not_processed_"+"offline_data"+"_"+str(int(random.random()*10000))+".csv"
		self.tweets_not_processed_file_path = os.path.join(path,self.tweets_not_processed_file_name)
		with open(self.tweets_not_processed_file_path,'w',encoding='utf-8',newline='') as csv_file:


			headers = ['tweet_id','tweet_text']
			csv_writer = csv.writer(csv_file)
			csv_writer.writerow(headers)
			i=1
			for tweet in fetched_tweets:
				row = [str(i),tweet]
				csv_writer.writerow(row)
				print(i)
				print(tweet)
				i +=1
		return self.tweets_not_processed_file_path
	def get_not_processed_tweets_path(self):
		return self.tweets_not_processed_file_path
	def save_preprocessed_tweets(self):
		with open(self.tweets_not_processed_file_path,'r',encoding='utf-8') as csv_r_file:
			csv_reader = csv.reader(csv_r_file)
			path=r".\data"
			self.tweets_processed_file_path = os.path.join(path,\
													self.tweets_not_processed_file_name[:14]+\
													self.tweets_not_processed_file_name[18:])
			with open(self.tweets_processed_file_path,'w',encoding='utf-8',newline='') as csv_w_file:
				csv_writer = csv.writer(csv_w_file)
				csv_writer.writerow(['tweet_id','processed_tweet'])
				#skip headers
				next(csv_reader)
				for tweet in csv_reader:
					if(len(tweet)==2):
						processed_tweet = preprocess.preprocess_tweets("".join(tweet[1]))
						t = processed_tweet
						t=" ".join(t)
						csv_writer.writerow([tweet[0],t])

		return self.tweets_processed_file_path
