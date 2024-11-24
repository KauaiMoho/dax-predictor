from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

driver = webdriver.Chrome()
currHeight = driver.execute_script("return document.body.scrollHeight")

driver.get("https://finance.yahoo.com/quote/%5EGDAXI/news/")
wait = WebDriverWait(driver, 10)
loaded_articles = set()

output_file = "dax_yahoo.csv"
with open(output_file, "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["date", "title"])

def get_article_titles():
    return driver.find_elements(By.CSS_SELECTOR, "h3.clamp.yf-18q3fnf")
def get_article_link(header):
    return driver.find_element(By.XPATH,f"//*[@title='{header}']")

def scroll_to_load():
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)
    currHeight = driver.execute_script("return document.body.scrollHeight")
    return (currHeight != last_height)

def scroll_to_currHeight():
    driver.execute_script(f"window.scrollTo(0, {currHeight});")
    time.sleep(2)

while True:
    headers = [header.text for header in get_article_titles()]
    new_headers = [article for article in headers if article not in loaded_articles]
    if not new_headers:
        scrolled = scroll_to_load()
        if not scrolled:
            print("No more content to load. Exiting.")
            break
        continue

    # actions = ActionChains(driver)
    # actions.move_to_element(article)
    # actions.click(article)
    # actions.perform()
    for i, header in enumerate(new_headers):
        try:
            scroll_to_currHeight()
            article = get_article_link(header)
            article.click()
            time_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "time.byline-attr-meta-time")))
            datetime_value = time_element.get_attribute("datetime")
            visible_date = time_element.text
            with open(output_file, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([visible_date, header])
            driver.back()
            
        except Exception as e:
            print(f"Error processing article {i+1}: {e}")
            continue
        loaded_articles.add(header)
driver.quit()
