from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from bson.binary import Binary,BinaryVectorDtype
import numpy as np

model = SentenceTransformer('paraphrase-MiniLM-L12-v2')

client = MongoClient("mongodb+srv://fliprwinner:Ycrg9XioOs1rKAOR@cluster0.548c4.mongodb.net/?appName=mongosh+2.4.0")
db = client["safenews_1"]

global_news_collection = db["global_news"]
indian_news_collection = db["indian_news"]

for doc in global_news_collection.find():
    summary_text = doc.get("Summary")
    
    if summary_text:
        embedding = model.encode(summary_text, precision="float32").tolist()
                
        global_news_collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"embedding": embedding}} 
        )

for doc in indian_news_collection.find():
    summary_text = doc.get("Summary")
    
    if summary_text:
        embedding = model.encode(summary_text, precision="float32").tolist()
                
        indian_news_collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"embedding": embedding}} 
        )