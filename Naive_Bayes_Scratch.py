from Extract_tweets import Extract_tweets 
from collections import Counter
import Preprocessing as Preprocess
import os
import csv
import math
import pickle
import random

class MN_Naive_Bayes:
	def __init__(self):
		self.tweets = Extract_tweets()

	def extract_features(self,processed_tweets_file_path):
		# extract words from test tweets
		# also calculate various couting needed
		self.processed_test_tweets = []
		with open(processed_tweets_file_path,'r',encoding='utf-8') as csv_file:
			csv_reader = csv.reader(csv_file)
			next(csv_reader)
			for line in csv_reader:
				self.processed_test_tweets.append(line[1].split())
	def train_model(self):
		
		cnt_pos = Counter()
		cnt_neg = Counter()
		cnt_neu = Counter()
		pos = []
		neg = []
		neu = []
		preprocessed_train_tweets = []
		self.total_words_all=0
		self.total_words_pos =0
		self.total_words_neg =0
		self.total_words_neu = 0
		train_file_name = 'training_dataset.csv'
		path=r"./dataset"
		train_file_path = os.path.join(path,train_file_name)
		with open(train_file_path,'r',encoding='utf-8') as train_file:
			csv_reader = csv.reader(train_file)
			for line in csv_reader:
				processed_tweet = Preprocess.preprocess_tweets(line[1])
				# print(processed_tweet)
				if(line[0]=="neutral"):
					neu.append(processed_tweet)
				elif(line[0]=="positive"):
					pos.append(processed_tweet)
				elif(line[0]=="negative"):
					neg.append(processed_tweet)
				else:
					continue
			
			for tweet in neu:
				for word in tweet:
					cnt_neu[word] +=1;
					self.total_words_neu +=1	
					self.total_words_all +=1
			for tweet in pos:
				for word in tweet:
					cnt_pos[word] +=1;
					self.total_words_pos +=1
					self.total_words_all +=1

			for tweet in neg:
				for word in tweet:
					cnt_neg[word] +=1;
					self.total_words_neg +=1
					self.total_words_all +=1
			train_result_dict = {'positive':cnt_pos,'negative':cnt_neg,'neutral':cnt_neu}
			train_result_fname = 'train_results.pickle'
			path=r"."
			self.train_result_fpath = os.path.join(path,train_result_fname)
			with open(self.train_result_fpath,'wb') as p_file:
				pickle.dump(train_result_dict,p_file)

			# print("Neutral tweets list",neu)
			# for key,value in cnt_pos.items():
			# 	print(key+":",value)
			self.prior_prob_pos = math.log(len(pos)/(len(pos)+len(neg)+len(neu)))
			self.prior_prob_neg =math.log(len(neg)/(len(pos)+len(neg)+len(neu)))
			self.prior_prob_neu = math.log(len(neu)/(len(pos)+len(neg)+len(neu)))
			# print("Postive prior prob",self.prior_prob_pos)
			# print("Negative prior prob",self.prior_prob_neg)
			# print("Neutral prior prob",self.prior_prob_neu)
			# print("Total words in pos class",self.total_words_pos)
			# print("Total words in neg class",self.total_words_neg)
			# print("Total words in neu class",self.total_words_neu)
			# print("Total words in train file",self.total_words_all)

			# print("Positive tweets counts",cnt_pos)
			# print("Negative tweets counts",cnt_neg)
			# print("Neutral tweets counts",cnt_neu)

				# preprocessed_train_tweets.append(self.tweets.preprocess_tweets(line[1]))
		# print(preprocessed_train_tweets)




	def test_model(self,not_processed_path):
		# calculate probabilites of feature 
		# calculate posterior probabilities
		# consider class with highest probabilities
		pos_words = []
		neg_words = []
		neu_words = []
		denom_pos = self.total_words_pos + self.total_words_all
		denom_neg = self.total_words_neg + self.total_words_all
		denom_neu = self.total_words_neu + self.total_words_all
		pos_like_dict = {}#positive likelihood dictionary
		neg_like_dict = {}#negative likelihood dictionary
		neu_like_dict = {}#neutral likelihood dictionary
		with open(self.train_result_fpath,'rb') as p_file:
			result_dict = pickle.load(p_file)
			for key,value in result_dict.items():
				if(key == 'positive'):
					for word,count in value.items():
						pos_words.append(word)
					# print("postive key")
				elif(key == 'negative'):
					for word,count in value.items():
						neg_words.append(word)
				elif(key == 'neutral'):
					for word,count in value.items():
						neu_words.append(word)


			# print("positive words in test total of"+ str(len(pos_words)) +"words",pos_words)
			# print("negative words in test total of"+ str(len(neg_words)) +"words" ,neg_words)
			# print("neutral words in test total of"+ str(len(neu_words))+ "words",neu_words)
			polarities = []
			pos_count=0
			neg_count=0
			neu_count=0
			c=0
			for tweet in self.processed_test_tweets:
				pos_like = 0
				neg_like = 0
				neu_like = 0
				pos_posterior = 0
				neg_posterior = 0
				neu_posterior = 0
				for word in tweet:
					if((word in pos_words) or (word in neg_words) or (word in neu_words)):
						pos_like=pos_like + math.log((result_dict['positive'][word]+1)/denom_pos)
						neg_like=neg_like + math.log((result_dict['negative'][word]+1)/denom_neg)
						neu_like=neu_like + math.log((result_dict['neutral'][word]+1)/denom_neu)

					else:
						continue
				pos_posterior = self.prior_prob_pos + pos_like
				neg_posterior = self.prior_prob_neg + neg_like
				neu_posterior = self.prior_prob_neu + neu_like
				max_prob = max(pos_posterior,neg_posterior,neu_posterior)

				c+=1
				print(c)
				print(" ".join(tweet))
				# print("pos ",pos_posterior)
				# print("neg",neg_posterior)
				# print("neu",neu_posterior)
				# print("max_prob",max_prob)		
				if(abs(max_prob-pos_posterior)<=0.000000000000000000000000001):
					polarities.append('positive')
					print("positive")
				elif(abs(max_prob-neg_posterior)<=0.000000000000000000000000001):
					polarities.append('negative')
					print("negative")

				elif(abs(max_prob-neu_posterior)<=0.000000000000000000000000001):
					polarities.append('neutral')
					print("neutral")


				
				print("\n")

			with open(not_processed_path,'r',encoding='utf-8') as csv_file:
				csv_reader = csv.reader(csv_file)
				next(csv_reader)
				result_file_name = 'Results_tweets_'+str(int((random.random()*10000)))+".csv"
				path=r"./data"
				result_file_path = os.path.join(path,result_file_name)
				header = ['tweet_id','tweet_text','polarity']
				with open(result_file_path,'w',encoding='utf-8',newline='') as out_file:
					csv_out_writer = csv.writer(out_file)
					csv_out_writer.writerow(header)
					i=0
					for line in csv_reader:
						if(line):
							row = [line[0],line[1],polarities[i]]
							if(polarities[i]=='neutral'):
								neu_count+=1
							elif(polarities[i]=='positive'):
								pos_count+=1
							else:
								neg_count+=1
							csv_out_writer.writerow(row)
						i +=1
						with open("akriti_pie_data.pickle",'wb') as f:
							pickle.dump([pos_count,neg_count,neu_count],f)
		return result_file_path



				



	


	
# test_class = MN_Naive_Bayes()
# test_class.train_model()
# test_class.extract_features()
# test_class.test_model()
