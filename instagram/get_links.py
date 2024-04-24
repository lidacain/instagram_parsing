import os
import csv
import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()
UserName = os.getenv('USERNAME')
PassWrd = os.getenv('PASSWORD')

def login(driver):
    loglink = "https://www.instagram.com/accounts/login/"
    username = UserName
    password = PassWrd

    driver.get(loglink)
    driver.implicitly_wait(3)

    usernameh = driver.find_element(By.NAME, 'username')
    usernameh.send_keys(username)

    passwordh = driver.find_element(By.NAME, 'password')
    passwordh.send_keys(password)

    driver.implicitly_wait(3)
    passwordh.submit()
    time.sleep(5)

def get_post_links(driver, profile_url, max_scroll_attempts=170):
    driver.get(profile_url)
    time.sleep(5)

    post_links = set()  # Use a set to avoid duplicates

    for _ in range(max_scroll_attempts):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Wait for the new content to load
        try:
            element_present = EC.presence_of_element_located((By.TAG_NAME, 'a'))
            WebDriverWait(driver, 10).until(element_present)
        except Exception as e:
            print(e)

        # Extract post links
        soup = bs(driver.page_source, 'html.parser')
        links = soup.find_all('a')
        new_post_links = set([link['href'] for link in links if '/p/' in link['href']])
        post_links.update(new_post_links)

        if len(new_post_links) == 0:
            break  # Break if no new links are found

    return [post_link[3:-1] for post_link in post_links]

def save_post_links_to_file(post_links, file_name):
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        for link in post_links:
            writer.writerow([link])

def main():
    driver = webdriver.Chrome()
    login(driver)

    profile_url = 'https://www.instagram.com/vindiesel/'
    max_scroll_attempts = 170
    post_links = get_post_links(driver, profile_url, max_scroll_attempts)

    file_name = 'post_links.csv'
    save_post_links_to_file(post_links, file_name)

    driver.quit()

if __name__ == "__main__":
    main()
