# from Extract_tweets import Extract_tweets
from Extract_tweets_offline import Extract_tweets_offline
from Naive_Bayes_Scratch import MN_Naive_Bayes
def get_tweets(query):
	# fetch_tweets = Extract_tweets()
	fetch_tweets=Extract_tweets_offline()
	# fetch_tweets.authenticate()

	path_not_processed = fetch_tweets.get_tweets(query)
	path_processed = fetch_tweets.save_preprocessed_tweets()
	return classify_tweets(path_processed,path_not_processed)

def classify_tweets(path_processed,path_not_processed):
	naive_bayes_classifier = MN_Naive_Bayes()
	naive_bayes_classifier.extract_features(path_processed)
	naive_bayes_classifier.train_model()
	result_file_path=naive_bayes_classifier.test_model(path_not_processed)
	return (result_file_path)

if __name__ == 'main':
	print("hello")
	get_tweets("nepal")