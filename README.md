# Intell-News: Autonomous News Aggregator & Summarizer 

## **🎯 Overview**
This project is an **autonomous AI agent** designed to search, summarize, and publish content on general news topics such as current events, crime, sports, politics, and more. The system operates at both **global** and **local levels**, extracting data from reliable sources, generating concise summaries, optimizing content for SEO, and publishing articles autonomously on a blog or website.

✨ **Bonus Feature**: We’ve integrated **AI-generated visuals** into the workflow! Using the **Stable Diffusion model**, the system generates relevant images in real-time based on the summaries of the articles. These images enhance the visual appeal of the blog posts and improve user engagement. 🖼️

The project leverages advanced technologies like **web scraping**(Selenium), **natural language processing (NLP)**, **MongoDB Atlas Search**, **Sentence Transformers**, and **Gemini API** for summarization and **RAG (Retrieval-Augmented Generation)** . 🚀

---

## **✨ Key Features**
- **🌐 Automated Web Crawling & Data Extraction**:
  - Fetched news articles from reliable sources such as BBC, Yahoo, New York Times (global), and Indian Express (local).
  - Classifies broader topics into sub-topics (e.g., Cities, Sports, Politics etc).
  
- **📝 Summarization & Content Generation**:
  - Utilizes MongoDB's Atlas Search feature to extract text.
  - Employs token embeddings to fetch data that corresponds to the user's prompt.
  - Processes extracted text into concise, well-structured summaries.
  - Ensures factual accuracy and coherence.

- **📈 SEO Optimization**:
  - Incorporates keywords, metadata, and readability improvements.
  - Generates engaging titles and descriptions for better search engine rankings.

- **🤖 Automated Publishing**:
  - Formats and publishes articles on a blog/website without manual intervention.
  - Ensures visually appealing and easy-to-read output.

- **🌟 Bonus Features**:
  - **Open-Source LLMs**: Used Sentence Transformers for vector embeddings instead of proprietary APIs.
  - **RAG Implementation**: Leveraged MongoDB Atlas Search for efficient retrieval of relevant data.
  - **Frontend Integration**: Built a user-friendly interface using HTML, CSS, and JavaScript.
  - Image Generation**: Uses the **Stable Diffusion model** to generate relevant images in real-time from article summaries, Enhances blog posts with visually appealing infographics.

---

## **🛠️ Technologies Used**
- **Web Scraping**: Selenium (initially explored Scrapy but dropped it due to limitations). 🕷️
- **Database**: MongoDB Atlas (with Atlas Search for RAG implementation). 🗄️
- **NLP Models**:
  - **Sentence Transformers**: Open-source model for generating vector embeddings. 🧠
  - **Gemini API**: For summarizing extracted text. ✍️
- **Image Generation**: Stable Diffusion model for real-time image creation from summaries. 🖼️
- **Backend**: Flask for integrating APIs and handling requests. 💻
- **Frontend**: HTML, CSS, and JavaScript for the user interface. 🌐
- **Deployment**: Hosted on Render. ☁️

---

## **⚙️ Project Workflow**

### **🔍 Step 1: Web Scraping**
- We used **Selenium** to scrape news articles from reliable sources:
  - **Global News Sources**: BBC, Yahoo, New York Times.
  - **Local News Sources**: Indian Express (India-specific news).
  
  _💡 Initially, we explored **Scrapy** for web scraping but decided against it due to its limitations in handling dynamic websites. Selenium allowed us to extract data from both static and dynamic pages efficiently._

---

### **🗄️ Step 2: Data Storage**
- All scraped data was stored in a **MongoDB Atlas** database.
- We utilized **Atlas Search** to implement **RAG (Retrieval-Augmented Generation)**:
  - Extracted text was converted into vector embeddings using **Sentence Transformers**.
  - Atlas Search indexed these embeddings, enabling efficient retrieval of the most relevant articles based on user queries.

---

### **📝 Step 3: Summarization**
- For summarization, we integrated **Gemini API** with our backend:
  - When a user provides a query, the system searches the MongoDB database for the best-rated vectors corresponding to the query.
  - The retrieved data is passed to the Gemini API, which generates concise and coherent summaries.

---

### **🖼️ Step 4: Image Generation**
- To enhance the blog posts with visuals, we implemented **Stable Diffusion**, an open-source text-to-image generation model:
  - The generated summaries are used as prompts for the Stable Diffusion model.
  - The model creates high-quality, contextually relevant images in real-time.
  - These images are automatically attached to the corresponding blog posts before publishing.

---

### **📈 Step 5: SEO Optimization**
- To ensure the generated articles rank well in search engines:
  - Keywords were identified and incorporated naturally into the content.
  - Meta tags, titles, and descriptions were optimized for better discoverability.
  - Readability improvements were made using libraries like **textstat**.

---

### **🤖 Step 6: Automated Publishing**
- The summarized articles, along with the AI-generated images, were formatted and published autonomously:
  - The backend (Flask) handled the formatting and integration with the frontend.
  - Articles were displayed on a user-friendly interface built using **HTML, CSS, and JavaScript**.

---

## **📦 Installation & Setup**

### **📋 Prerequisites**
- Python 3.9+ 🐍
- MongoDB Atlas account 🗃️
- Flask installed (`pip install flask`) 💻
- Sentence Transformers (`pip install sentence-transformers`) 🧠
- Gemini API key ✍️
- Stable Diffusion model setup (self-hosted or via Hugging Face) 🖼️

### **🚀 Steps**
1. Clone the repository:
   ```bash
   git clone https://github.com/Ayush-Singh677/IntelliNews
   cd IntelliNews
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up MongoDB Atlas:
   - Create a free-tier cluster on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas). 🌐
   - Enable **Atlas Search** and configure indexes for vector embeddings.

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the frontend:
   - Open `index.html` in your browser or deploy the app on a cloud platform. ☁️

---

## **🔮 Future Enhancements**
- **🌍 Multilingual Support**: Add translation capabilities to publish articles in multiple languages (e.g., Hindi, English). 🌐
- **🎨 Enhanced Image Customization**: Allow users to customize the style and format of AI-generated images. 🖌️
- **📊 User Engagement Metrics**: Track article views, shares, and search rankings to measure performance. 📈

---

## **👥 Contributors**
- [Ayush singh](https://github.com/Ayush-Singh677) 👩‍💻
- [Arsh Vats](https://github.com/arsh0429) 👨‍💻


---
