import os
import pandas as pd
from pymongo import MongoClient
from utils import scrape_yahoo_news

yahoo_df = scrape_yahoo_news()
yahoo_df.to_csv("data/yahoo_news_dataset.csv", index=False)
print("Yahoo News dataset saved as yahoo_news_dataset.csv")

# data_dir = "data"
# all_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.csv')]

# df_list = [pd.read_csv(file) for file in all_files]
# merged_df = pd.concat(df_list, ignore_index=True)

# categories = merged_df['Category'].unique()
# category_dfs = {category: merged_df[merged_df['Category'] == category] for category in categories}

# client = MongoClient('mongodb://localhost:27017/')
# db = client['news_database']

# for category, df in category_dfs.items():
#     collection = db[category] 
#     records = df.to_dict('records')
#     collection.insert_many(records)
#     print(f"Inserted {len(records)} records into {category} collection")

# print("Data has been successfully pushed to MongoDB.")