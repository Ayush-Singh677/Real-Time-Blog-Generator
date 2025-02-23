import os
import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb+srv://fliprwinner:Ycrg9XioOs1rKAOR@cluster0.548c4.mongodb.net/?appName=mongosh+2.4.0")
db = client["safenews_1"]

global_news_collection = db["global_news"]
indian_news_collection = db["indian_news"]

def upload_csv_to_mongodb(csv_file_path, is_global):
    try:
        df = pd.read_csv(csv_file_path)

        if 'Category' not in df.columns or 'Headline' not in df.columns or 'Summary' not in df.columns:
            print(f"Error: Missing required columns in {csv_file_path}")
            return

        records = df.to_dict(orient='records')

        collection = global_news_collection if is_global else indian_news_collection

        for record in records:
            category = record.get('Category', '').lower()

            record['is_global'] = is_global
            record['Category'] = category

            collection.insert_one(record)
            print(f"Inserted record into {collection.name} (Category: {category}): {record['Headline']}")

    except Exception as e:
        print(f"Error processing {csv_file_path}: {e}")

def process_all_csv_files(global_directory, indian_directory):
    for filename in os.listdir(global_directory):
        if filename.endswith(".csv"):
            csv_file_path = os.path.join(global_directory, filename)
            print(f"Processing global news file: {csv_file_path}")
            upload_csv_to_mongodb(csv_file_path, is_global=True)

    for filename in os.listdir(indian_directory):
        if filename.endswith(".csv"):
            csv_file_path = os.path.join(indian_directory, filename)
            print(f"Processing Indian news file: {csv_file_path}")
            upload_csv_to_mongodb(csv_file_path, is_global=False)

if __name__ == "__main__":
    global_csv_directory = "scrapper/data/global"
    indian_csv_directory = "scrapper/data/Indian"

    process_all_csv_files(global_csv_directory, indian_csv_directory)
