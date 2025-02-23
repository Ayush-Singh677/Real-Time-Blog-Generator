from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
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


def scrape_yahoo_news():
    """
    Scrape news articles from Yahoo News.
    Returns a DataFrame containing the scraped data.
    """
    driver = setup_driver()
    driver.get("https://news.yahoo.com/")
    time.sleep(3)  # Wait for initial load
    
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