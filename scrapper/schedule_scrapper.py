import os
import time
import re
from datetime import date, datetime
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
        By.XPATH, '//div[@class="carousel-item active"] //td[@class="text-left bg-white"] //b'
    )
    date_parced = re.search(r'([0-9]+(\.[0-9]+)+)', week_element.text)
    if date_parced is None:
        raise Exception('No data parced')
    date_object = datetime.strptime(date_parced.group(0), '%d.%m.%Y').isocalendar()[1]
    current_week = date.today().isocalendar()[1]
    carousel_next = driver.find_element(
            By.CSS_SELECTOR, '.carousel-control-next'
        )
    if date_object == current_week:
        return None
    carousel_next.click()
    time.sleep(2)
    validate_week(driver)


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
