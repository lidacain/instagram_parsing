import os
import time
import csv
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from datetime import datetime

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


def extract_data(driver, postlink):
    post_url = f'https://www.instagram.com/p/{postlink}/'
    driver.get(post_url)
    time.sleep(4)

    soup = bs(driver.page_source, 'html.parser')

    description_div = soup.find('div', class_='x5yr21d xw2csxc x1odjw0f x1n2onr6')
    description_text = ''
    if description_div:
        description = description_div.find('h1')
        if description and description.text:
            description_text = description.text[:50]
            description_text = description_text + '...' if len(description.text) > 50 else description_text
    print(description_text)
    date_element = soup.find('time', class_='_aaqe')
    date_published_str = date_element['title'] if date_element else ''

    date_published_str = date_published_str.strip()  # Удаление пробелов по краям строки

    # Проверка на количество пробелов в дате для определения формата
    if date_published_str.count(' ') > 1:
        try:
            date_parts = date_published_str.split()
            months = {
                'январь': '01', 'февраль': '02', 'март': '03', 'апрель': '04', 'май': '05', 'июнь': '06',
                'июль': '07', 'август': '08', 'сентябрь': '09', 'октябрь': '10', 'ноябрь': '11', 'декабрь': '12'
            }
            formatted_date = f"{int(date_parts[0]):02d}.{months[date_parts[1].lower()]}.{date_parts[2]}"
            date_published = formatted_date
        except Exception as e:
            print(f"Error occurred while processing full date format: {e}")
            date_published = ''
    else:
        try:
            date_parts = date_published_str.split()
            months = {
                'январь': '01', 'февраль': '02', 'март': '03', 'апрель': '04', 'май': '05', 'июнь': '06',
                'июль': '07', 'август': '08', 'сентябрь': '09', 'октябрь': '10', 'ноябрь': '11', 'декабрь': '12'
            }
            if len(date_parts) == 2:  # Если указан только месяц и день
                day = int(date_parts[0])
                month = months.get(date_parts[1].lower())
                year = datetime.now().year  # Получаем текущий год
                date_published = f"{day:02d}.{month}.{year}"
            else:  # Иначе, ошибка в данных
                raise ValueError("Invalid date format")
        except Exception as e:
            print(f"Error occurred while processing abbreviated date format: {e}")
            date_published = ''

    likes_span = soup.find('span', class_='html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs')
    likes = likes_span.text.replace("\xa0", "") if likes_span else ''

    return [post_url, description_text, date_published, likes]


def write_data_to_csv(data, output_filename):
    with open(output_filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)


def collect_data(driver, filename, output_filename):
    with open(filename, 'r') as f:
        post_links = [line.strip() for line in f]

    for postlink in post_links:
        data = extract_data(driver, postlink)
        write_data_to_csv(data, output_filename)


if __name__ == "__main__":
    driver = webdriver.Chrome()
    login(driver)

    collect_data(driver, 'post_links_1.csv', 'metadatas.csv')
