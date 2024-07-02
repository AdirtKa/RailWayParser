import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


WAGON: str = 'Цистерны для нефти'
DEPARTURE_STATION: str = '654909'
OPERATION_STATION: str = '828501'
CARGO: str = '20100'


def parse_data(page_source: str) -> list[int]:
    soup: BeautifulSoup = BeautifulSoup(page_source, 'html.parser')
    result: list[int] = []
    for value in soup.find(class_='form-result').find_all(class_='form-result__col__value')[1:3]:
        result += value.text.split(' ')[0]
    return result


def enter_param() -> str:
    driver = webdriver.Chrome()
    driver.get('https://spimex.com/markets/oil_products/rzd/')

    driver.implicitly_wait(2)

    driver.find_elements(By.CLASS_NAME, 'terms__footer__btn')[0].click()
    driver.find_element(By.CLASS_NAME, 'cookie-agree__button').click()

    driver.find_element(By.NAME, 'wagon').send_keys(WAGON + Keys.RETURN)

    driver.find_element(By.NAME, 'station_from').send_keys(DEPARTURE_STATION)
    driver.find_element(By.CLASS_NAME, 'form__col-1-2').find_element(By.TAG_NAME, 'li').click()

    driver.find_element(By.NAME, 'station_to').send_keys(OPERATION_STATION)
    driver.find_elements(By.CLASS_NAME, 'form__col-1-2')[1].find_element(By.TAG_NAME, 'li').click()

    driver.find_element(By.NAME, 'product').send_keys(CARGO)
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, 'form__col-1-1').find_element(By.TAG_NAME, 'li').click()

    driver.find_element(By.CLASS_NAME, 'form__submit').click()

    time.sleep(1)
    driver.close()
    return driver.page_source


if __name__ == '__main__':
    traveled_distance, traveled_time = parse_data(enter_param())
    print(traveled_distance, traveled_time, sep=' ')
    