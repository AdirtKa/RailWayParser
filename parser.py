import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


WAGON: str = 'Цистерны для нефти'
CARGO: str = '21400'


def parse_data(page_source: str) -> list[int]:
    soup: BeautifulSoup = BeautifulSoup(page_source, 'html.parser')
    result: list[int] = []
    for value in soup.find(class_='form-result').find_all(class_='form-result__col__value')[1:3]:
        numeric_part = ''
        for potential_num in value.text.split():
            if potential_num.isnumeric():
                numeric_part += potential_num

        result.append(int(numeric_part))

    return result


def enter_param(departure_station: str, operation_station: str) -> str:
    driver = webdriver.Chrome()
    driver.get('https://spimex.com/markets/oil_products/rzd/')

    driver.implicitly_wait(2)

    driver.find_elements(By.CLASS_NAME, 'terms__footer__btn')[0].click()
    driver.find_element(By.CLASS_NAME, 'cookie-agree__button').click()

    driver.find_element(By.NAME, 'wagon').send_keys(WAGON + Keys.RETURN)

    driver.find_element(By.NAME, 'station_from').send_keys(departure_station.split(' ')[0])
    driver.find_element(By.CLASS_NAME, 'form__col-1-2').find_element(By.TAG_NAME, 'li').click()

    driver.find_element(By.NAME, 'station_to').send_keys(operation_station.split(' ')[0])
    driver.find_elements(By.CLASS_NAME, 'form__col-1-2')[1].find_element(By.TAG_NAME, 'li').click()

    driver.find_element(By.NAME, 'product').send_keys(CARGO)
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, 'form__col-1-1').find_element(By.TAG_NAME, 'li').click()

    driver.find_element(By.CLASS_NAME, 'form__submit').click()

    time.sleep(1)
    page_source = driver.page_source
    driver.close()
    return page_source


if __name__ == '__main__':
    print(parse_data(enter_param('654909', '873308')))
