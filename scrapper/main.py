from utils import scrape_yahoo_news
import pandas as pd

yahoo_df = scrape_yahoo_news()
yahoo_df.to_csv("yahoo_news_dataset.csv", index=False)
print("Yahoo News dataset saved as yahoo_news_dataset.csv")