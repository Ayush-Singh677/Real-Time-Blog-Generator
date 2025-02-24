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
    
    # Hide automation detection
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
        time.sleep(2)  # Wait for new content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


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
    Returns a DataFrame and writes the results to 'indianexpress_news.csv'.
    """
    driver = setup_driver()
    
    base_url = "https://indianexpress.com/section/"
    # List of categories to iterate over (appended to the base URL)
    categories_list = ["political-pulse", "cities", "sports",  "lifestyle"]
    
    all_categories = []
    all_titles = []
    all_summaries = []
    all_dates = []
    
    for cat in categories_list:
        url = base_url + cat
        print(f"Processing {url} ...")
        driver.get(url)
        time.sleep(3)  # Wait for page load
        
        scroll_down(driver)
        
        # Locate all articles on the page
        articles = driver.find_elements(By.CSS_SELECTOR, "div.articles")
        print(f"Found {len(articles)} articles in {cat}")
        
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
                # Skip articles if any element is missing
                continue

    driver.quit()
    
    df = pd.DataFrame({
        "Category": all_categories,
        "Headline": all_titles,
        "Summary": all_summaries,
        "Date": all_dates
    })
    
    df.to_csv("indianexpress_news.csv", index=False)
    return df

def scrape_reuters_news():
    """
    Scrape news articles from bbc News.
    Returns a DataFrame containing the scraped data.
    """
    driver = setup_driver()
    driver.get("https://reuters.com/")
    time.sleep(3)
    
    scroll_down(driver)
    
    # Extract the cluster category from the header (used as a fallback)
    cluster_category = driver.find_element(
        By.CSS_SELECTOR,
        'section[data-testid="story-cluster"] h2[data-testid="story-clusterSectionNameHeading"] a'
    ).text.strip()

    # Find all story cards within the cluster
    articles = driver.find_elements(By.CSS_SELECTOR, 'li[data-testid="StoryCard"]')

    # Lists to store the extracted details
    categories = []
    titles = []
    links = []
    summaries = []
    dates = []

    for article in articles:
        try:
            # Extract the title and link from the story card
            title_link_element = article.find_element(By.CSS_SELECTOR, 'a[data-testid="TitleLink"]')
            title = title_link_element.find_element(
                By.CSS_SELECTOR, 'span[data-testid="TitleHeading"]'
            ).text.strip()
            link = title_link_element.get_attribute("href")
            
            # Extract the summary/description
            summary_element = article.find_element(By.CSS_SELECTOR, 'p[data-testid="Description"]')
            summary = summary_element.text.strip() if summary_element else "No summary available"
            
            # Extract the datetime (from the <time> element)
            time_element = article.find_element(By.CSS_SELECTOR, 'time[data-testid="DateLineText"]')
            date = time_element.get_attribute("datetime")
            
            # Attempt to extract a specific category (kicker) if present; else, use the cluster category
            try:
                category = article.find_element(By.CSS_SELECTOR, 'span[data-testid="KickerLabel"]').text.strip()
            except Exception:
                category = cluster_category
            
            # Append the extracted information to the lists
            categories.append(category)
            titles.append(title)
            summaries.append(summary)
            dates.append(date)
        except Exception as e:
            continue
        
        driver.quit()
        
        df = pd.DataFrame({
            "Category": categories,
            "Headline": titles,
            "Summary": summaries,
            "Dates": date
        })
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
