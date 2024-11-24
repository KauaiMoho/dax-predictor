from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

driver = webdriver.Chrome()
driver.get("https://www.tradingview.com/news-flow/?symbol=XETR:DAX")

headers = driver.find_elements(By.CSS_SELECTOR, "div.apply-overflow-tooltip.apply-overflow-tooltip--direction_both.block-bETdSLzM.title-HY0D0owe.title-DmjQR0Aa")
header_texts = [header.text for header in headers]
times = driver.find_elements(By.CSS_SELECTOR, "relative-time.apply-common-tooltip")
time_texts = [time.get_attribute('event-time') for time in times]
count = 0

output_file = 'dax_tradingview.csv'


with open(output_file, mode='a', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["date", "title"])
    writer.writeheader()
    for i in range(len(header_texts)):
        writer.writerow({'date': time_texts[i], 'title': header_texts[i]})

print(f"Adding {len(header_texts)} elements.")
driver.quit()