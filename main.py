import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


departure_station = '654909'
operation_station = '828501'
cargo = '20100'


def main() -> None:
    driver = webdriver.Chrome()
    driver.get('https://spimex.com/markets/oil_products/rzd/')

    driver.implicitly_wait(2)

    user_agreement = driver.find_elements(By.CLASS_NAME, 'terms__footer__btn')[0]
    user_agreement.click()

    organization_info = driver.find_element(By.CLASS_NAME, 'cookie-agree__button')
    organization_info.click()

    wagon_elem = driver.find_element(By.NAME, 'wagon')
    wagon_elem.send_keys('Цистерны для нефти' + Keys.RETURN)

    departure_station_elem = driver.find_element(By.NAME, 'station_from')
    departure_station_elem.send_keys(departure_station)

    driver.find_element(By.CLASS_NAME, 'form__col-1-2').find_element(By.TAG_NAME, 'li').click()

    operation_station_elem = driver.find_element(By.NAME, 'station_to')
    operation_station_elem.send_keys(operation_station)

    driver.find_elements(By.CLASS_NAME, 'form__col-1-2')[1].find_element(By.TAG_NAME, 'li').click()

    cargo_elem = driver.find_element(By.NAME, 'product')
    cargo_elem.send_keys(cargo)

    time.sleep(1)

    driver.find_element(By.CLASS_NAME, 'form__col-1-1').find_element(By.TAG_NAME, 'li').click()

    driver.find_element(By.CLASS_NAME, 'form__submit').click()

    time.sleep(10)
    driver.close()


if __name__ == '__main__':
    main()
