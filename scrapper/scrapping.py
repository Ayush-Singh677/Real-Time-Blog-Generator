import os
import pandas as pd
from pymongo import MongoClient
from utils import scrape_bbc_news,scrape_yahoo_news, scrape_indian_express, scrape_nytimes_world_news

yahoo_df = scrape_yahoo_news()
yahoo_df.to_csv("data/global/yahoo_news_dataset.csv", index=False)
print("Yahoo News dataset saved as yahoo_news_dataset.csv")

bbc_df=scrape_bbc_news()
bbc_df=bbc_df.drop(index=1)
bbc_df.to_csv("data/global/bbc_news_dataset.csv", index=False)
print("bbc News dataset saved as bbc_news_dataset.csv")

indian_express_df=scrape_indian_express()
indian_express_df=indian_express_df.drop(index=1)
indian_express_df.to_csv("data/indian/Indian_express_news_dataset.csv", index=False)
print("Indian express News dataset saved as indian_express_news_dataset.csv")

nytimes_df=scrape_nytimes_world_news()
nytimes_df=nytimes_df.drop(index=1)
nytimes_df.to_csv("data/global/nytimes_news.csv", index=False)
print("NY Times News dataset saved as nytimes_news.csv")
