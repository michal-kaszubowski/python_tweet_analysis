import string
import re
import pandas as pd
import nltk
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from wordcloud import WordCloud


def analyze():
    stop_words = set(stopwords.words("english"))
    punctuation = set(string.punctuation)
    regex = re.compile('[^a-zA-Z]')
    lem = WordNetLemmatizer()

    filtered = []
    standardized = []

    with open('reddits/lastYear.txt', 'r') as file:
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
    freq_dist_df.to_csv('reddits/freqDistLastYear.csv')

    joined = ' '.join(standardized)

    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(joined)
    wordcloud.to_file('reddits/imgsLastYear.png')


analyze()
