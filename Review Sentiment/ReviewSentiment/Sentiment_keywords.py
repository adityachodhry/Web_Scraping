import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from collections import Counter
from word2number import w2n

def is_numerical_word(word):
    try:
        num_value = w2n.word_to_num(word)  
        return True
    except ValueError:
        return False

def extract_keywords(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))

    # # Additional hotelname tokens to be excluded
    # hotelname_tokens = set(word_tokenize(hotelname.lower()))

    special_characters = set(['|', '#', "'", ')', '!', ';', '[', '?', '.', '&', '@', ']', '+', '=', '/', '_', '-', '~', '*', ':', '>', ',', '<', '}', '^', '\\', '`', '(', '$', '{', '%', '"', '``', '...', '....', "''", '..', "'s"])
    adjectives = {'JJ', 'JJR', 'JJS'}
    adverbs = {'RB', 'RBR', 'RBS'}
    pronoun_tags = {'PRP', 'PRP$'}
    indefinite_pronouns = {'another', 'anybody', 'anyone', 'anything', 'each', 'either', 'enough', 'everybody', 'everyone', 'everything', 'few', 'many', 'neither', 'nobody', 'none', 'no one', 'nothing', 'one', 'several', 'somebody', 'someone', 'something', 'such','hotel'}

    lemmatizer = WordNetLemmatizer()

    filtered_tokens = [word for word, pos in pos_tag(tokens) 
                       if len(word) > 1  # Exclude single-letter words
                       and not word.isdigit()  # Exclude numerical values
                       and not is_numerical_word(word.lower())  # Exclude English numbers
                       and word.lower() not in stop_words  # Exclude stop words
                       and word not in special_characters  # Exclude special characters
                       and pos not in adjectives  # Exclude adjectives
                       and pos not in adverbs  # Exclude adverbs
                       and pos not in {'DT', 'PRP', 'MD'}  # Exclude determiners, object pronouns, and modal verbs
                       and lemmatizer.lemmatize(word, pos='v') == word  # Exclude irregular verbs
                       and word.lower() not in indefinite_pronouns  # Exclude indefinite pronouns
                       and pos not in pronoun_tags  # Exclude words with pronoun POS tags
                       and pos not in {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}  # Exclude verbs
                    #    and word.lower() not in hotelname_tokens  # Exclude words from hotelname
    ]

    word_freq = Counter(filtered_tokens)
    return list(word_freq.keys())[:5]  # Return top 5 keywords

def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(text)
    
    if sentiment_scores['compound'] >= 0.05:
        sentiment_type = 'Positive'
    elif sentiment_scores['compound'] <= -0.05:
        sentiment_type = 'Negative'
    else:
        sentiment_type = 'Neutral'
    
    sentiment_score = round((sentiment_scores['compound'] + 1) * 5, 2)  
    
    return sentiment_type, sentiment_score

with open('Novotel_reviews_all.json', 'r') as json_file:
    all_reviews = json.load(json_file)

processed_reviews = []

for review in all_reviews['reviews']:
    reviewId = review.get('reviewId')
    reviewContent = review.get('reviewText')

    print(reviewContent)
    if reviewContent and isinstance(reviewContent, str) and reviewContent.strip():
        sentiment_type, sentiment_score = analyze_sentiment(reviewContent)
        keywords = extract_keywords(reviewContent)

        processed_review = {
            'hId' : 20001,
            'reviewId': reviewId,
            'sentimentType': sentiment_type,
            'sentimentScore': sentiment_score,
            'keywords': keywords
        }

        processed_reviews.append(processed_review)

with open('Novotel.json', 'w') as outfile:
    json.dump(processed_reviews, outfile, indent=4)
