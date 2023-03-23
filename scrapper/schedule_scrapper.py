import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from alchemy import session, Entry


load_dotenv()

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
# Define window size to get full, not cropped screenshot
chrome_options.add_argument('--window-size=1920,1200')

url = 'https://cabinet.vvsu.ru'


def get_schedule_current():
    print('Scrapper started.')
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Remote(
        command_executor='http://selenium:4444/wd/hub',
        options=chrome_options
    )
    driver.get(url)
    time.sleep(4)

    login_field = driver.find_element(By.ID, 'login')
    login_field.send_keys(os.getenv('LOGIN'))

    password_field = driver.find_element(By.ID, 'password')
    password_field.send_keys(os.getenv('PASSWORD'))

    time.sleep(2)

    button = driver.find_element(By.ID, 'accept')
    button.click()

    time.sleep(2)

    timetable_button = driver.find_element(By.CSS_SELECTOR, '.red')
    timetable_button.click()
    time.sleep(2)

    html_main = driver.find_element(By.TAG_NAME, 'html')
    html_main.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    timetable = driver.find_element(By.TAG_NAME, 'table')
    timetable.screenshot(f'{os.getcwd()}/schedule.png')
    driver.delete_all_cookies()
    driver.close()
    driver.quit()
    # Update last entry time
    entry = session.query(Entry).filter(Entry.id == 1).one()
    entry.update_time()
