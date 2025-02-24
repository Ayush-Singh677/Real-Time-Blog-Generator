from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

def setup_driver():
    """
    Set up and return a Selenium WebDriver instance with appropriate options.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """
    })
    return driver


def scroll_down(driver):
    """
    Scroll down the page to load all content dynamically.
    """
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def scrape_nytimes_world_news():
    """
    Scrape news articles from The New York Times World section.
    Extracts headlines and summaries from pages 2 to 20.
    Returns a DataFrame and writes the results to 'nytimes_world_news.csv'.
    """
    driver = setup_driver()
    base_url = "https://www.nytimes.com/international/section/world?page="
    
    all_titles = []
    all_summaries = []
    
    for page_number in range(2, 21):  
        url = f"{base_url}{page_number}"
        print(f"Processing {url} ...")
        driver.get(url)
        time.sleep(3)  
        
        scroll_down(driver)
        

        articles = driver.find_elements(By.CSS_SELECTOR, "li.css-18yolpw article.css-1l4spti")
        print(f"Found {len(articles)} articles on page {page_number}")
        
        for article in articles:
            try:
        
                title_element = article.find_element(By.CSS_SELECTOR, "a.css-8hzhxf h3.css-1j88qqx.e15t083i0")
                title = title_element.text.strip() if title_element else ""
                
                if not title or title.isspace():
                    print("Skipping article with empty title.")
                    continue
                
               
                summary_element = article.find_element(By.CSS_SELECTOR, "p.css-1pga48a.e15t083i1")
                summary = summary_element.text.strip() if summary_element else "No summary available"
                
 
                all_titles.append(title)
                all_summaries.append(summary)
                
                print(f"Scraped article: {title}")
            except Exception as e:
                print(f"Error processing an article: {e}")
                continue
    
    driver.quit()

    df = pd.DataFrame({
        "Category": ["World"] * len(all_titles), 
        "Headline": all_titles,
        "Summary": all_summaries
    })
    

    df.to_csv("nytimes_world_news.csv", index=False)
    print(f"Dataset saved as nytimes_world_news.csv with {len(all_titles)} articles.")
    return df

def scrape_bbc_news():
    """
    Scrape news articles from bbc News.
    Returns a DataFrame containing the scraped data.
    """
    driver = setup_driver()
    driver.get("https://bbc.com/")
    time.sleep(3)
    
    scroll_down(driver)
    
    titles = []
    summaries = []
    categories = []
    
    articles = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="card-text-wrapper"]')
    for article in articles:
        try:
            title_element = article.find_element(By.CSS_SELECTOR, 'h2[data-testid="card-headline"]')
            title = title_element.text.strip()

            summary_element = article.find_element(By.CSS_SELECTOR, 'p[data-testid="card-description"]')
            summary = summary_element.text.strip() if summary_element else "No summary available"

            category_element = article.find_element(By.CSS_SELECTOR, 'span[data-testid="card-metadata-tag"]')
            category = category_element.text.strip() if category_element else "No category"

            categories.append(category)
            titles.append(title)
            summaries.append(summary)
        except Exception as e:
            continue
    
    driver.quit()
    
    df = pd.DataFrame({
        "Category": categories,
        "Headline": titles,
        "Summary": summaries
    })
    return df


def scrape_indian_express():
    """
    Scrape news articles from the Indian Express section pages for each specified category.
    Extracts the title, summary, and date for each article.
    Returns a DataFrame and appends the results to 'indianexpress_news.csv'.
    """
    driver = setup_driver()
    
    base_url = "https://indianexpress.com/section/"

    categories_list = ["political-pulse", "cities", "sports", "lifestyle"]
    
    all_categories = []
    all_titles = []
    all_summaries = []
    all_dates = []
    
    for cat in categories_list:
        for page in range(1, 21):  
            url = f"{base_url}{cat}/page/{page}/" if page > 1 else f"{base_url}{cat}"
            print(f"Processing {url} ...")
            driver.get(url)
            time.sleep(3) 
            
            scroll_down(driver)
            
            articles = driver.find_elements(By.CSS_SELECTOR, "div.articles")
            print(f"Found {len(articles)} articles in {cat} on page {page}")
            
            for article in articles:
                try:
                    title_element = article.find_element(By.CSS_SELECTOR, "div.img-context h2.title a")
                    title = title_element.text.strip()
                    
                    summary_element = article.find_element(By.CSS_SELECTOR, "div.img-context p")
                    summary = summary_element.text.strip()
                    
                    date_element = article.find_element(By.CSS_SELECTOR, "div.img-context div.date")
                    date = date_element.text.strip()
                    
                    all_categories.append(cat)
                    all_titles.append(title)
                    all_summaries.append(summary)
                    all_dates.append(date)
                except Exception as e:
                    continue
    
    driver.quit()
    
    df = pd.DataFrame({
        "Category": all_categories,
        "Headline": all_titles,
        "Summary": all_summaries,
        "Date": all_dates
    })
    
    try:
        existing_df = pd.read_csv("indianexpress_news.csv")
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        combined_df.to_csv("indianexpress_news.csv", index=False)
    except FileNotFoundError:
        df.to_csv("indianexpress_news.csv", index=False)
    
    return df


def scrape_yahoo_news():
    """
    Scrape news articles from Yahoo News.
    Returns a DataFrame containing the scraped data.
    """
    driver = setup_driver()
    driver.get("https://news.yahoo.com/")
    time.sleep(3)
    
    scroll_down(driver)
    
    titles = []
    links = []
    summaries = []
    categories = []
    
    articles = driver.find_elements(By.CSS_SELECTOR, '[data-test-locator="stream-item"]')
    for article in articles:
        try:
            category = article.find_element(By.CSS_SELECTOR, 'strong[data-test-locator="stream-item-category-label"]').text.strip()
            title_element = article.find_element(By.CSS_SELECTOR, 'h3[data-test-locator="stream-item-title"] a')
            title = title_element.text.strip()
            link = title_element.get_attribute("href")
            summary_element = article.find_element(By.CSS_SELECTOR, 'p[data-test-locator="stream-item-summary"]')
            summary = summary_element.text.strip() if summary_element else "No summary available"
            
            categories.append(category)
            titles.append(title)
            links.append(link)
            summaries.append(summary)
        except Exception as e:
            continue
    
    driver.quit()
    
    df = pd.DataFrame({
        "Category": categories,
        "Headline": titles,
        "Link": links,
        "Summary": summaries
    })
    return df
