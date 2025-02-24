import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import requests

genai.configure(api_key="AIzaSyA6PNAOL5xQS8xB6FXAcc_2zM9yRX5Ofjs")
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model_gemini = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)
model_sentence = SentenceTransformer('paraphrase-MiniLM-L12-v2')

client = MongoClient("mongodb+srv://fliprwinner:Ycrg9XioOs1rKAOR@cluster0.548c4.mongodb.net/?appName=mongosh+2.4.0")
db = client["safenews_1"]
global_news_collection = db["global_news"]
indian_news_collection = db["indian_news"]

app = Flask(__name__)
CORS(app)

TEMP_DIR = "main\\temp"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-blog', methods=['POST'])
def generate_blog():
    # try:
    data = request.get_json()
    blog_topic = data.get('topic', '')
    query_embedding = model_sentence.encode(blog_topic, precision="float32").tolist()
    pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "queryVector": query_embedding,
                    "path": "embedding",
                    "exact": True,
                    "limit": 15
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "Category": 1,
                    "Summary": 1,
                    "Headline": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ]
    print("Fetched queries from database.")
    text = ""
    results = global_news_collection.aggregate(pipeline)
    for result in results:
        text += f"Headline: {result['Headline']} Summary: {result['Summary']}\n"
    
    # print(text)
    prompt = (
            "You are a news agent expert in writing about news in blogs. Below are few headlines and summaries. "
            f"The user-given query is: {blog_topic}."
        )
    receding_prompt = (
            "Your job is to return the category, a good title in the first curly bracket and a detailed and coherent blog in the next curly bracket. "
            "Eg:{Category} {Title} {Blog}."
        )
    
    blog_response = model_gemini.generate_content(prompt + text + receding_prompt).text

    category = blog_response.split("{")[1].split("}")[0]
    title = blog_response.split("{")[2].split("}")[0]
    content = blog_response.split("{")[3].split("}")[0]

    stability_api_key = "sk-7Y9iay1XD83XUQNfkHbtt8mbGT9x4qtVGuk6re65T9CIB1G9"
    image_url = generate_image(title, stability_api_key)

    image_filename = "image.jpeg"
    image_path = os.path.join(TEMP_DIR, image_filename)
    os.rename(image_url, image_path)

    html_content = render_template('generated.html', category=category, title=title, content=content, image_url=image_filename)
    html_filename = "index.html"
    html_path = os.path.join(TEMP_DIR, html_filename)
    with open(html_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

    return jsonify({'blog_url': 'main/temp/generated.html'})

@app.route('/main/temp/<filename>')
def serve_temp_file(filename):
    print(f"Serving file: {filename} from {TEMP_DIR}")
    return send_from_directory(TEMP_DIR, filename)

def generate_image(prompt, api_key):
    """
    Generate an image using Stability AI's API.
    Returns the local path of the generated image.
    """
    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": prompt,
            "output_format": "jpeg",
        },
    )
    if response.status_code == 200:
        image_filename = "image.jpeg"
        image_path = os.path.join(TEMP_DIR,image_filename)
        with open(image_path, 'wb') as file:
            file.write(response.content)
        return image_path
    else:
        raise Exception(f"Image generation failed: {response.json()}")

if __name__ == '__main__':
    app.run(debug=True)
