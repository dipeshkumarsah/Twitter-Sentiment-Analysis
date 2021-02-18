import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
#call this function for all the preprocessiing
def preprocess_tweets(tweet):
	processed_tweet = []
	# Convert to lower case
	tweet = tweet.lower()
	# Replaces URLs with the word blank
	tweet = re.sub(r'((www\.[\S]+)|(https?://[\S]+))', ' ', tweet)
	# Replace @handle with the word blank
	tweet = re.sub(r'@[\S]+', ' ', tweet)
	# Replaces #hashtag with hashtag
	tweet = re.sub(r'#(\S+)', r' \1 ', tweet)
	# Remove RT (retweet)
	tweet = re.sub(r'\brt\b', '', tweet)
	# Replace 2+ dots with space
	tweet = re.sub(r'\.{2,}', ' ', tweet)
	# Strip space, " and ' from tweet
	tweet = tweet.strip(' "\'')
	# Replace emojis with either EMO_POS or EMO_NEG
	tweet = handle_emojis(tweet)
	# Replace multiple spaces with a single space
	tweet = re.sub(r'\s+', ' ', tweet)
	words = tweet.split()

	for word in words:
		word = preprocess_word(word)
		# lemmatize_word(word)
		if (is_valid_word(word) and (not(is_stop_word(word)))):
			processed_tweet.append(word)

	return processed_tweet

def preprocess_word(word):
    # Remove punctuation
    word = word.strip('\'"?!,.():;')
    # Convert more than 2 letter repetitions to 2 letter
    # funnnnny --> funny
    word = re.sub(r'(.)\1+', r'\1\1', word)
    # Remove - and '
    word = re.sub(r'(-|\')', '', word)
    return word


def is_valid_word(word):
    # Check if word begins with an alphabet
    return (re.search(r'^[a-zA-Z][a-z0-9A-Z\._]*$', word) is not None)


def handle_emojis(tweet):
    # Smile -- :), : ), :-), (:, ( :, (-:, :')
    tweet = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\))', ' EMO_POS ', tweet)
    # Laugh -- :D, : D, :-D, xD, x-D, XD, X-D
    tweet = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', ' EMO_POS ', tweet)
    # Love -- <3, :*
    tweet = re.sub(r'(<3|:\*)', ' EMO_POS ', tweet)
    # Wink -- ;-), ;), ;-D, ;D, (;,  (-;
    tweet = re.sub(r'(;-?\)|;-?D|\(-?;)', ' EMO_POS ', tweet)
    # Sad -- :-(, : (, :(, ):, )-:
    tweet = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', ' EMO_NEG ', tweet)
    # Cry -- :,(, :'(, :"(
    tweet = re.sub(r'(:,\(|:\'\(|:"\()', ' EMO_NEG ', tweet)
    return tweet
def lemmatize_word(word):
	wordnet_lemmatizer = WordNetLemmatizer()
	return wordnet_lemmatizer.lemmatize(word)


def is_stop_word(word):
	stops = set(stopwords.words('english'))
	if(word in stops):
		return True
	else:
		return False

