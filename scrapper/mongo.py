import os
import pandas as pd
from pymongo import MongoClient

# Step 1: Connect to MongoDB
client = MongoClient("mongodb+srv://fliprwinner:Ycrg9XioOs1rKAOR@cluster0.548c4.mongodb.net/?appName=mongosh+2.4.0")
db = client["safenews_1"]  # Replace with your database name

# Step 2: Define collections for global and Indian news
global_news_collection = db["global_news"]
indian_news_collection = db["indian_news"]

# Step 3: Function to process and upload CSV files
def upload_csv_to_mongodb(csv_file_path, is_global):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file_path)

        # Ensure required columns exist
        if 'Category' not in df.columns or 'Headline' not in df.columns or 'Summary' not in df.columns:
            print(f"Error: Missing required columns in {csv_file_path}")
            return

        # Convert DataFrame rows to dictionaries
        records = df.to_dict(orient='records')

        # Determine the target collection based on whether it's global or Indian
        collection = global_news_collection if is_global else indian_news_collection

        # Insert records into MongoDB, grouped by category
        for record in records:
            category = record.get('Category', '').lower()  # Normalize category to lowercase

            # Add metadata for better querying
            record['is_global'] = is_global
            record['Category'] = category

            # Insert the record into the appropriate collection
            collection.insert_one(record)
            print(f"Inserted record into {collection.name} (Category: {category}): {record['Headline']}")

    except Exception as e:
        print(f"Error processing {csv_file_path}: {e}")

# Step 4: Automate processing of all CSV files in a directory
def process_all_csv_files(global_directory, indian_directory):
    # Process global news CSV files
    for filename in os.listdir(global_directory):
        if filename.endswith(".csv"):
            csv_file_path = os.path.join(global_directory, filename)
            print(f"Processing global news file: {csv_file_path}")
            upload_csv_to_mongodb(csv_file_path, is_global=True)

    # Process Indian news CSV files
    for filename in os.listdir(indian_directory):
        if filename.endswith(".csv"):
            csv_file_path = os.path.join(indian_directory, filename)
            print(f"Processing Indian news file: {csv_file_path}")
            upload_csv_to_mongodb(csv_file_path, is_global=False)

# Step 5: Main execution
if __name__ == "__main__":
    # Specify the directories containing your global and Indian CSV files
    global_csv_directory = "C:/Users/Arsh/Desktop/SafeNews/scrapper/data/global"  # Replace with the path to your global CSV files
    indian_csv_directory = "C:/Users/Arsh/Desktop/SafeNews/scrapper/data/Indian"  # Replace with the path to your Indian CSV files

    process_all_csv_files(global_csv_directory, indian_csv_directory)
