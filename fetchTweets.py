import re
import pandas as pd
import snscrape.modules.twitter as sntwitter

scrap_queries_df = pd.read_csv("scrapQueries.csv")

for i in range(0, len(scrap_queries_df['query'])):
    report = "%s" % (i + 1) + "/" + "%s" % len(scrap_queries_df['query'])
    with open('tweets/%s.txt' % scrap_queries_df['name'][i], 'w') as file:
        for j, tweet in enumerate(sntwitter.TwitterSearchScraper(scrap_queries_df['query'][i]).get_items()):
            print(">@ %s" % j, " | %s" % report)
            if j >= 100_000:
                break
            file.write(re.sub(r'http\S+', '', tweet.content.replace('\n', ' ')))
            file.write('\n')
