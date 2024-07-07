import time
import re

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

from exceptions import UnreadbleStation, NoDataReceived


WAGON: str = 'Цистерны для нефти'
CARGO: str = '21400'
unreadable: list[str] = ['МАЛОКОВАЛИ (951176)', 'ПЕНЬКОВАЯ (950722)', 'УДАРНЫЙ (961411)', 'ИКУРА (962823)']


def check_exist(by: By, value: str, driver: WebDriver) -> bool:
    try:
        driver.find_element(by, value)
    except NoSuchElementException:
        return False
    return True


def scroll_to_element(element: WebElement, driver: WebDriver) -> WebElement:
    ActionChains(driver) \
        .scroll_to_element(element) \
        .perform()
    return element


def parse_data_rzd_cargo(page_source: str) -> list[int]:
    soup: BeautifulSoup = BeautifulSoup(page_source, 'html.parser')
    result: list[int] = []
    for value in soup.find_all(class_='content-opt__value')[2:4]:
        numeric_part = ''
        for potential_num in value.text:
            if potential_num.isnumeric():
                numeric_part += potential_num

        result.append(int(numeric_part, 10))

    return result


def parse_data_spimex(page_source: str) -> list[int]:
    soup: BeautifulSoup = BeautifulSoup(page_source, 'html.parser')
    result: list[int] = []
    for value in soup.find(class_='form-result').find_all(class_='form-result__col__value'):
        print(value.text)
    for value in soup.find(class_='form-result').find_all(class_='form-result__col__value')[1:3]:
        numeric_part = ''
        for potential_num in value.text:
            if potential_num.isnumeric():
                numeric_part += potential_num

        result.append(int(numeric_part, 10))

    return result


def enter_param_rzd_cargo(departure_station: str, operation_station: str) -> list[int]:
    if any(item == operation_station for item in unreadable):
        raise UnreadbleStation(operation_station)
    if any(item == departure_station for item in unreadable):
        raise UnreadbleStation(departure_station)

    options = webdriver.EdgeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')
    options.add_argument('--no-sandbox')

    driver = webdriver.Edge(options=options)
    driver.get('https://cargo.rzd.ru/ru/9803')

    scroll_to_element(driver.find_element(By.NAME, 'FROM'), driver).send_keys(re.findall(r'(\d+)',
                                                                                         departure_station)[0])

    scroll_to_element(driver.find_element(By.NAME, 'TO'), driver).send_keys(re.findall(r'(\d+)',
                                                                                       operation_station)[0]
                                                                            + Keys.RETURN)

    flag = False
    while not flag:
        flag = check_exist(By.CLASS_NAME, 'content-opt__value', driver)
        if driver.find_element(By.ID, 'js__error_result').is_displayed():
            raise NoDataReceived(departure_station, operation_station)

    page_source = driver.page_source
    driver.close()
    return parse_data_rzd_cargo(page_source)


def enter_param_spimex(departure_station: str, operation_station: str) -> list[int]:
    if any(item == operation_station for item in unreadable):
        raise UnreadbleStation(operation_station)
    if any(item == departure_station for item in unreadable):
        raise UnreadbleStation(departure_station)

    options = webdriver.EdgeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')
    options.add_argument('--no-sandbox')

    driver = webdriver.Edge(options=options)
    driver.get('https://spimex.com/markets/oil_products/rzd/')

    driver.implicitly_wait(2)

    scroll_to_element(driver.find_elements(By.CLASS_NAME, 'terms__footer__btn')[0], driver).click()
    scroll_to_element(driver.find_element(By.CLASS_NAME, 'cookie-agree__button'), driver).click()

    scroll_to_element(driver.find_element(By.NAME, 'wagon'), driver).send_keys(WAGON + Keys.RETURN)

    scroll_to_element(driver.find_element(By.NAME, 'station_from'), driver).send_keys(departure_station.split('(')[0])
    time.sleep(1)
    scroll_to_element(driver.find_element(By.CLASS_NAME, 'form__col-1-2').find_element(By.TAG_NAME, 'li'),
                      driver).click()

    scroll_to_element(driver.find_element(By.NAME, 'station_to'), driver).send_keys(operation_station.split(' ')[0])
    time.sleep(1)
    driver.find_elements(By.CLASS_NAME, 'form__col-1-2')[1].find_element(By.TAG_NAME, 'li').click()

    scroll_to_element(driver.find_element(By.NAME, 'product'), driver).send_keys(CARGO)
    time.sleep(1)
    scroll_to_element(driver.find_element(By.CLASS_NAME, 'form__col-1-1'), driver).find_element(By.TAG_NAME,
                                                                                                'li').click()

    scroll_to_element(driver.find_element(By.CLASS_NAME, 'form__submit'), driver).click()

    time.sleep(1)
    page_source = driver.page_source
    driver.close()
    return parse_data_spimex(page_source)


if __name__ == '__main__':
    print('result: ', enter_param_rzd_cargo('654909', ''))
