# Real Time Blog Generator

## **Overview**
This project presents an autonomous AI system designed to search, summarize, and publish content on general news topics, including current events, crime, sports, politics, and more. The system operates at both global and local levels, extracting data from reliable sources, generating concise summaries, optimizing content for search engine visibility, and autonomously publishing articles on a blog or website.

**Bonus Feature**: This system integrates AI-generated visuals into the publishing workflow. Using the Stable Diffusion model, the system produces relevant images in real time based on article summaries. These visuals enhance the presentation and engagement of the published content.

The project utilizes advanced technologies such as web scraping (Selenium), Natural Language Processing (NLP), MongoDB Atlas Search, Sentence Transformers, the Gemini API for summarization, and Retrieval-Augmented Generation (RAG).

---

## **Key Features**

### **Automated Web Crawling & Data Extraction**
- Retrieves news articles from trusted sources, including:
  - Global: BBC, Yahoo, New York Times
  - Local (India-specific): Indian Express
- Classifies news into structured sub-topics such as Cities, Sports, and Politics.

### **Summarization & Content Generation**
- Utilizes MongoDB Atlas Search to access and extract relevant textual content.
- Applies vector embeddings to retrieve content that matches user prompts.
- Generates structured, concise summaries that maintain factual accuracy and coherence.

### **SEO Optimization**
- Incorporates targeted keywords, metadata, and improvements to article readability.
- Generates engaging titles and descriptions to enhance search engine performance.

### **Automated Publishing**
- Automatically formats and publishes articles on a blog or website.
- Ensures a clean, user-friendly, and visually coherent presentation.

### **Additional Functionalities**
- **Open-Source LLMs**: Leverages Sentence Transformers for embedding generation instead of closed-source APIs.
- **Retrieval-Augmented Generation**: Implements RAG using MongoDB Atlas Search for high-quality, relevant article retrieval.
- **Frontend Integration**: User interface is developed using HTML, CSS, and JavaScript.
- **Image Generation**: Uses Stable Diffusion to generate relevant and visually compelling images from summary content, enhancing article presentation.

---

## **Technologies Used**
- **Web Scraping**: Selenium (preferred over Scrapy due to better handling of dynamic websites)
- **Database**: MongoDB Atlas with integrated Atlas Search functionality
- **NLP Components**:
  - Sentence Transformers for embedding generation
  - Gemini API for summarizing textual content
- **Image Generation**: Stable Diffusion for creating contextually relevant images in real time
- **Backend**: Flask, used to manage APIs and backend logic
- **Frontend**: HTML, CSS, and JavaScript
- **Deployment**: Hosted on Render

---

## **Project Workflow**

### **Step 1: Web Scraping**
- News content is extracted using Selenium from global (BBC, Yahoo, New York Times) and local (Indian Express) sources.
- Scrapy was initially considered, but Selenium was chosen for its superior ability to interact with dynamic web pages.

### **Step 2: Data Storage**
- Extracted content is stored in MongoDB Atlas.
- Atlas Search is used to enable Retrieval-Augmented Generation:
  - Text data is converted into vector embeddings using Sentence Transformers.
  - These embeddings are indexed in MongoDB to support fast and relevant content retrieval based on user queries.

### **Step 3: Summarization**
- The system uses the Gemini API for content summarization:
  - When a query is received, vector search retrieves relevant content from MongoDB.
  - This data is then passed to the Gemini API to generate accurate and concise summaries.

### **Step 4: Image Generation**
- Stable Diffusion, an open-source text-to-image model, is used to generate visuals:
  - Summarized text serves as input prompts for image generation.
  - The model creates contextually appropriate, high-quality images in real time.
  - Generated visuals are automatically attached to their respective articles before publishing.

### **Step 5: SEO Optimization**
- Search engine visibility is improved through:
  - Incorporation of relevant keywords.
  - Generation of optimized meta tags, titles, and descriptions.
  - Enhancing content readability using tools like textstat.

### **Step 6: Automated Publishing**
- The backend, developed with Flask, handles content formatting and frontend integration.
- Final content, including AI-generated summaries and images, is published through a responsive and clean HTML, CSS, and JavaScript frontend.

---

## **Installation & Setup**

### **Prerequisites**
- Python 3.9 or higher
- MongoDB Atlas account
- Flask (`pip install flask`)
- Sentence Transformers (`pip install sentence-transformers`)
- Gemini API access
- Stable Diffusion model (can be hosted locally or via Hugging Face)

### **Setup Instructions**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Ayush-Singh677/Real-Time-Blog-Generator
   cd Real-Time-Blog-Generator

2. **Install the required Python packages**:
      ```bash
   pip install -r requirements.txt

3. **Configure MongoDB Atlas**:
-Set up a free-tier cluster on MongoDB Atlas
-Enable Atlas Search and configure vector indexes.

4. **Run the application**:
   ```bash
   python app.py
   
6. **Open the frontend**:

-Open the index.html file in your browser or deploy the application to a cloud platform of your choice.

## **Future Enhancements**
-Multilingual Support: Add capabilities to publish articles in multiple languages, such as Hindi and English.
-Advanced Image Customization: Allow users to define image styles and formats before generation.
-User Engagement Metrics: Integrate analytics to track article views, shares, and SEO performance.

## **Contributors**:-
- [Ayush singh](https://github.com/Ayush-Singh677) 
- [Arsh Vats](https://github.com/arsh0429) 
