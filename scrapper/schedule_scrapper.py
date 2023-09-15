import os
import time
import re
from datetime import date
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

load_dotenv()

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
# Define window size to get full, not cropped screenshot
chrome_options.add_argument('--window-size=1400,1400')

url = 'https://cabinet.vvsu.ru'


def validate_week(driver: webdriver.Remote) -> None:
    """Validate current week"""
    week_element = driver.find_element(
        By.XPATH, '//td[@class="text-left bg-white"] //b'
    ).text
    remote_week = re.search(r'\d+', week_element)
    current_date = date.today()
    carousel_next = driver.find_element(
            By.CSS_SELECTOR, '.carousel-control-next'
        )
    while True:
        if abs(int(current_date.strftime('%d'))-int(remote_week.group(0))) <= 7\
        or abs(int(current_date.strftime('%d'))-int(remote_week.group(0))) == 0:
            return None
        carousel_next.click()
        time.sleep(1)


def screenshot_tt(driver: webdriver.Remote, is_next: bool = False) -> None:
    """ Screenshot table element containing schedule """
    timetable = driver.find_element(
        By.XPATH, '//div[@class="carousel-item active"]'
    )
    timetable.screenshot(
        f"{os.getcwd()}/schedule{(lambda: '-next' if is_next else '')()}.png"
    )


def get_schedule_screenshots():
    print('Scrapper started.')
    # Connect to the Selenium Standalone
    driver = webdriver.Remote(
        command_executor='http://selenium:4444/wd/hub',
        options=chrome_options
    )
    driver.get(url)
    time.sleep(4)
    # Fill the login field
    login_field = driver.find_element(By.ID, 'login')
    login_field.send_keys(os.getenv('LOGIN'))
    # Fill the password field
    password_field = driver.find_element(By.ID, 'password')
    password_field.send_keys(os.getenv('PASSWORD'))

    time.sleep(2)

    button = driver.find_element(By.ID, 'accept')
    button.click()

    time.sleep(2)
    # Open schedule page
    timetable_button = driver.find_elements(By.CSS_SELECTOR, '.main-nav-link')[2]
    timetable_button.click()
    time.sleep(2)
    #validate current week
    validate_week(driver)
    # Send "Page Down" in case the timetable does not fit in the visible area
    html_main = driver.find_element(By.TAG_NAME, 'html')
    html_main.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    # Make a screenshot
    screenshot_tt(driver)
    # Next week schedule
    carousel_next = driver.find_element(
        By.CSS_SELECTOR, '.carousel-control-next'
    )
    carousel_next.click()
    time.sleep(1)
    screenshot_tt(driver, is_next=True)

    # I don't know if it is necessary to clean all the cookies, but anyway :-)
    driver.delete_all_cookies()
    driver.close()
    driver.quit()
