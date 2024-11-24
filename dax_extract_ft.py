from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import pandas as pd

driver = webdriver.Chrome()
output_file = 'dax_ft.csv'

with open(output_file, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["date", "title"])
        writer.writeheader()
        for i in range(1,101):
            driver.get(f"https://www.ft.com/germany?page={i}")
            headers = driver.find_elements(By.CSS_SELECTOR, "a.js-teaser-heading-link")
            header_texts = [header.text for header in headers]
            times = driver.find_elements(By.CSS_SELECTOR, "time.o-date")
            time_texts = [time.text for time in times]
            for j in range(len(header_texts)):
                writer.writerow({'date': time_texts[j], 'title': header_texts[j]})
            time.sleep(1)
            print(f"Added {i}/101 pages.")
driver.quit()