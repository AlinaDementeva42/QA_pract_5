import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os

# Добавляем путь к папке locators
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from locators import saucedemo_locators as loc

BASE_URL = "https://www.saucedemo.com/"

def login(driver, username="standard_user", password="secret_sauce"):
    driver.get(BASE_URL)
    driver.find_element(By.CSS_SELECTOR, loc.USERNAME_INPUT).send_keys(username)
    driver.find_element(By.CSS_SELECTOR, loc.PASSWORD_INPUT).send_keys(password)
    driver.find_element(By.CSS_SELECTOR, loc.LOGIN_BUTTON).click()

# Сценарий 1: Успешная покупка
def test_successful_purchase(driver):
    login(driver)
    driver.find_element(By.CSS_SELECTOR, loc.ADD_TO_CART_BACKPACK).click()
    driver.find_element(By.CSS_SELECTOR, loc.CART_ICON).click()
    driver.find_element(By.CSS_SELECTOR, loc.CHECKOUT_BUTTON).click()
    driver.find_element(By.CSS_SELECTOR, loc.FIRST_NAME_INPUT).send_keys("John")
    driver.find_element(By.CSS_SELECTOR, loc.LAST_NAME_INPUT).send_keys("Doe")
    driver.find_element(By.CSS_SELECTOR, loc.ZIP_CODE_INPUT).send_keys("123456")
    driver.find_element(By.CSS_SELECTOR, loc.CONTINUE_BUTTON).click()
    driver.find_element(By.CSS_SELECTOR, loc.FINISH_BUTTON).click()
    success_text = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, loc.SUCCESS_HEADER))
    ).text
    assert "Thank you for your order!" in success_text

# Сценарий 2: Очистка корзины
def test_cart_clearing(driver):
    login(driver)
    driver.find_element(By.CSS_SELECTOR, loc.ADD_TO_CART_BACKPACK).click()
    driver.find_element(By.CSS_SELECTOR, loc.CART_ICON).click()
    driver.find_element(By.CSS_SELECTOR, loc.REMOVE_BACKPACK).click()
    badge_elements = driver.find_elements(By.CSS_SELECTOR, loc.CART_BADGE)
    assert len(badge_elements) == 0, "Корзина не пуста!"

# Сценарий 3: Неуспешная авторизация
def test_invalid_login(driver):
    driver.get(BASE_URL)
    driver.find_element(By.CSS_SELECTOR, loc.USERNAME_INPUT).send_keys("invalid_user")
    driver.find_element(By.CSS_SELECTOR, loc.PASSWORD_INPUT).send_keys("wrong_password")
    driver.find_element(By.CSS_SELECTOR, loc.LOGIN_BUTTON).click()
    error_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, loc.ERROR_MESSAGE))
    ).text
    assert "Username and password do not match" in error_msg