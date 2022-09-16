import string
import re
import pandas as pd
import nltk
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.stem.wordnet import WordNetLemmatizer
from wordcloud import WordCloud

scrap_queries_df = pd.read_csv("scrapQueries.csv")


def analyze():
    stop_words = set(stopwords.words("english"))
    stop_words.add('nt')
    stop_words.add('lt')
    stop_words.add('rt')

    punctuation = set(string.punctuation)
    regex = re.compile('[^a-zA-Z]')
    lem = WordNetLemmatizer()

    for i in range(0, len(scrap_queries_df['query'])):
        print(">@ %s" % (i + 1) + "/" + "%s" % len(scrap_queries_df['query']))
        filtered = []
        standardized = []

        with open('tweets/%s.txt' % scrap_queries_df['name'][i], 'r') as file:
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
        freq_dist_df.to_csv('freqDist/f%s.csv' % scrap_queries_df['name'][i])

        joined = ' '.join(standardized)

        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(joined)
        wordcloud.to_file('imgs/f%s.png' % scrap_queries_df['name'][i])


analyze()
