from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

driver = webdriver.Chrome()
driver.get("https://finance.yahoo.com/quote/%5EGDAXI/news/")

last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

headers = driver.find_elements(By.CSS_SELECTOR, "h3.clamp.yf-18q3fnf")
header_texts = [header.text for header in headers]
redirs = driver.find_elements(By.CSS_SELECTOR, "a.subtle-link.fin-size-small.titles.noUnderline.yf-1e4diqp")
links = [elem.get_attribute('href') for elem in redirs]
count = 0

output_file = 'dax_yahoo.csv'

try:
    with open(output_file, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["date", "title"])
        writer.writeheader()
        for url in links:
            print(f"Processing link {count+1} out of {len(links)}.")
            driver.get(url)
            wait = WebDriverWait(driver, 10)
            time_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "time.byline-attr-meta-time")))
            datetime_value = time_element.get_attribute("datetime")
            writer.writerow({'date': time_element.text, 'title': header_texts[count]})
            count+=1
            time.sleep(1)
            if(count >= 200):
                print(f"Stopping at max {count} links.")
                break
except Exception as exc:
    print(exc)

driver.quit()