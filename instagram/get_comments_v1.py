import os
import time
import csv
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

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


def PostComments(driver, postlink):
    # Открыть Instagram пост
    post_url = f'https://www.instagram.com/p/{postlink}/'
    driver.get(post_url)
    time.sleep(4)  # Подождать загрузки страницы

    # Получить HTML-код страницы после загрузки
    soup = bs(driver.page_source, 'html.parser')

    # Найти все div комментариев
    comments_div = soup.find_all('div', class_='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1')

    comments = []
    for div in comments_div:
        spans = div.find_all('span', class_='_ap3a _aaco _aacu _aacx _aad7 _aade')
        for span in spans:
            comment_text = span.text.strip()  # Извлекаем текст комментария
            comments.append(comment_text)

    return comments


def WriteComments(comment_list, output_filename):
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Comments"])
        for comment in comment_list:
            writer.writerow([comment])


def FullComments(driver, filename):
    comment_list = []

    with open(filename, 'r') as f:
        post_links = [line.strip() for line in f]

    for postlink in post_links:
        comments = PostComments(driver, postlink)
        comment_list.extend(comments)

    return comment_list


if __name__ == "__main__":
    driver = webdriver.Chrome()
    login(driver)

    post_links = []
    with open('post_links_1.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            post_links.extend(row)

    comment_list = FullComments(driver, 'post_links_1.csv')
    WriteComments(comment_list, 'comments.csv')
