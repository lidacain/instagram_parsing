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
    # Оставляем вашу функцию login без изменений
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


def get_post_links(driver, profile_url, max_posts=100):
    # Ваша функция get_post_links без изменений
    driver.get(profile_url)
    time.sleep(5)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup = bs(driver.page_source, 'html.parser')
    links = soup.find_all('a')
    post_links = [link['href'] for link in links if '/p/' in link['href']][:max_posts]
    return [post_link[3:-1] for post_link in post_links]


def PostComments(driver, postlink):
    # Ваша функция PostComments без изменений
    post_url = f'https://www.instagram.com/p/{postlink}/'
    driver.get(post_url)
    time.sleep(5)

    soup = bs(driver.page_source, 'html.parser')
    comments_span = soup.find_all('span', class_='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj')
    comments = [comment.text for comment in comments_span]

    return comments


def WriteComments(comment_list, output_filename):
    # Ваша функция WriteComments без изменений
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Comments"])
        for comment in comment_list:
            writer.writerow([comment])


if __name__ == "__main__":
    driver = webdriver.Chrome()
    login(driver)

    # Получаем URL-адреса постов и записываем их в файл post_links_1.csv
    profile_url = 'https://www.instagram.com/vindiesel/'
    post_links = get_post_links(driver, profile_url)
    with open('post_links_1.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for link in post_links:
            writer.writerow([link])

    # Извлекаем комментарии из сохраненных URL-адресов постов
    comment_list = []
    with open('post_links_1.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            post_links.extend(row)

    for postlink in post_links:
        comments = PostComments(driver, postlink)
        comment_list.extend(comments)

    # Записываем комментарии в файл comments.csv
    WriteComments(comment_list, 'comments.csv')

    driver.quit()
