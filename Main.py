import cgi
from Extract_tweets import Extract_tweets
from Naive_Bayes_Scratch import MN_Naive_Bayes
def get_tweets(query):
	# query = cgi.FieldStorage().getvalue('searchbox')
	fetch_tweets = Extract_tweets()
	fetch_tweets.authenticate()

	path_not_processed = fetch_tweets.get_tweets(query)
	path_processed = fetch_tweets.save_preprocessed_tweets()
	classify_tweets(path_processed,path_not_processed)

def classify_tweets(path_processed,path_not_processed):
	naive_bayes_classifier = MN_Naive_Bayes()
	naive_bayes_classifier.extract_features(path_processed)
	naive_bayes_classifier.train_model()
	naive_bayes_classifier.test_model(path_not_processed)

if __name__ == 'main':
	print("hello")
	get_tweets("nepal")
	# url="http://localhost:8080/search_result.php?data="+cgi.FieldStorage().getvalue('searchbox')
	# webbrowser.open(url,new=0, autoraise=True)
