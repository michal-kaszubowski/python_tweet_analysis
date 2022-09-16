import string
import re
import pandas as pd
import nltk
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from wordcloud import WordCloud
import text2emotion as te
from nltk.sentiment import SentimentIntensityAnalyzer


def basic():
    stop_words = set(stopwords.words("english"))
    punctuation = set(string.punctuation)
    regex = re.compile('[^a-zA-Z]')
    lem = WordNetLemmatizer()

    filtered = []
    standardized = []

    with open('tweets/sample.txt', 'r') as file:
        data = file.read()
        file.close()
    tokens = nltk.word_tokenize(data)

    for word in tokens:
        if word.lower() not in stop_words and word.lower() not in punctuation:
            filtered.append(regex.sub('', word.lower()))

    for word in filtered:
        if len(word) > 1:
            standardized.append(lem.lemmatize(word, "v"))

    freq_dist = FreqDist(standardized)
    fq_to_frame = {'words': freq_dist.keys(), 'occurrences': freq_dist.values()}
    freq_dist_df = pd.DataFrame(fq_to_frame)
    freq_dist_df.to_csv('freqDist/sampleFreqDist.csv')

    joined = ' '.join(standardized)

    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(joined)
    wordcloud.to_file('imgs/sample.png')


def count():
    sid = SentimentIntensityAnalyzer()
    sid_likes = 0
    sid_dislikes = 0
    positive_tweets = []
    negative_tweets = []
    positive_emotions = {'Angry': 0.0, 'Fear': 0.0, 'Happy': 0.0, 'Sad': 0.0, 'Surprise': 0.0}
    negative_emotions = {'Angry': 0.0, 'Fear': 0.0, 'Happy': 0.0, 'Sad': 0.0, 'Surprise': 0.0}

    with open('tweets/sample.txt', 'r') as file:
        lines = file.readlines()
        file.close()

    for line in lines:
        ss = sid.polarity_scores(line)
        if ss['pos'] > ss['neg']:
            sid_likes += 1
        else:
            sid_dislikes += 1

        emotions = te.get_emotion(line)
        if emotions['Happy'] + emotions['Surprise'] < emotions['Angry'] + emotions['Sad'] + emotions['Fear']:
            negative_tweets.append(line)
            for emotion in emotions.keys():
                negative_emotions[emotion] += emotions[emotion]
        else:
            positive_tweets.append(line)
            for emotion in emotions.keys():
                positive_emotions[emotion] += emotions[emotion]

    sid_to_frame = {'overall': sid_likes + sid_dislikes, 'positive': sid_likes, 'negative': sid_dislikes}
    ss_df = pd.DataFrame(data=sid_to_frame, index=[0])
    ss_df.to_csv('sentiment/sid/sample.csv')

    sorted_positive = {k: v for k, v in sorted(positive_emotions.items(), key=lambda item: item[1])}
    sorted_negative = {k: v for k, v in sorted(negative_emotions.items(), key=lambda item: item[1])}

    positive_to_frame = {
        'overall': len(positive_tweets) + len(negative_tweets),
        'positive': len(positive_tweets),
        'main': list(sorted_positive.keys())[-1],
        'secondary': list(sorted_positive.keys())[-2]
    }
    negative_to_frame = {
        'overall': len(positive_tweets) + len(negative_tweets),
        'negative': len(negative_tweets),
        'main': list(sorted_negative.keys())[-1],
        'secondary': list(sorted_negative.keys())[-2]
    }

    positive_df = pd.DataFrame(data=positive_to_frame, index=[0])
    negative_df = pd.DataFrame(data=negative_to_frame, index=[0])

    positive_df.to_csv('sentiment/tex2emo/positiveSample.csv')
    negative_df.to_csv('sentiment/tex2emo/negativeSample.csv')


basic()
count()
