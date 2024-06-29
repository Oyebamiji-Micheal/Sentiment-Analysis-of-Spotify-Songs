import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Ensure NLTK resources are available
try:
    nltk.data.find('corpora/stopwords.zip')
    nltk.data.find('tokenizers/punkt.zip')
    nltk.data.find('corpora/wordnet.zip')
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('vader_lexicon')

# Extend the list of stopwords
stop_words = stopwords.words('english')
stop_words.extend([
    'verse', 'chorus', 'i"ll', 'intro', 'outro', 'or', 'm', 'ma', 'ours', 'against', 'nor',
    'wasn', 'hasn', 'my', 'had', 'didn', 'isn', 'did', 'aren', 'those', 'than', 'man'
    "mustn't", "you've", 'to', 'she', 'having', "haven't", 'into', 't', 'll', 
    'himself', 'do', "that'll", 'so', 'of', 'on', 'very', 'for', 'out', 'were', 
    'should', 'they', 'ain', "should've", 'you', "didn't", 'yours', 'was', 'our',
     'can', 'myself', "shouldn't", 'have', 'up', 'mightn', "you'll", 'any', 
    'itself', 'hadn', 'him', 'doesn', 'weren', 'y', 'being', "don't", 'them', 
    'are','and', 'that', 'your', 'yourself', 'their', 'some', 'ourselves', 've', 
    'doing', 'been', 'shouldn', 'yourselves', "mightn't", 'most', 'because',
     'few', 'wouldn', "you'd", 'through', "you're", 'themselves', 'an', 'if',
     "wouldn't", 'its', 'other', "won't", "wasn't", "she's", 'we', 'shan',
     "weren't",'don',"hadn't", 'this', 'off', 'while', 'a', 'haven', 'her', 
    'theirs', 'all', "hasn't", "doesn't", 'about', 'then', 'by','such', 'but', 
    'until', 'each', 'there', "aren't", 'with', 'not', "shan't", 'hers', 'it', 
    'too', 'i', 'at', 'is', 'as', 'me', 'herself', 's', 'the', 'where', 'am', 
    'has', 'over', "couldn't", 'when', 'does', 'mustn','re', 'no', 'in', 'who', 
    'd', 'own', 'he', 'be', "isn't", 'his', 'these', 'same', 'whom', 'will', 
    'needn','couldn', 'from',  "it's", 'o', 'yeah','ya','na','wan','uh','gon',
    'ima','mm','uhhuh','bout','em','nigga','niggas','got','ta','lil','ol','hey',
    'oooh','ooh','oh','youre','dont','im','youve','ive','theres','ill','yaka',
    'lalalala','la','da','di','yuh', 'shawty','oohooh','shoorah','mmmmmm',
    'ook','bidibambambambam','shh','bro','ho','aint','cant','know','bambam',
    'shitll','tonka'
])

stop_words = set(stop_words)

# Pre-compile the regex pattern for removing escaped new line characters
newline_pattern = re.compile(r'\\n')

# Initialize lemmatizer 
lemmatizer = WordNetLemmatizer()

def preprocess_lyrics(lyrics):
    # Remove escaped new line character
    lyrics = newline_pattern.sub(' ', str(lyrics))
    
    # Tokenization
    tokens = word_tokenize(lyrics)
    
    # Process tokens: remove punctuation, convert to lowercase, remove stopwords, and lemmatize
    processed_tokens = [
        lemmatizer.lemmatize(word.lower())
        for word in tokens if word.isalpha() and word.lower() not in stop_words
    ]
    
    return ' '.join(processed_tokens)

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(lyrics):
    scores = analyzer.polarity_scores(lyrics)
    compound_score = scores['compound']
    if compound_score > 0:
        sentiment = 'positive'
    elif compound_score < 0:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    return compound_score, sentiment
