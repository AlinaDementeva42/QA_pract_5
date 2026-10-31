import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os
import allure

# Добавляем путь к папке locators
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from locators import saucedemo_locators as loc

BASE_URL = "https://www.saucedemo.com/"


@allure.feature("Авторизация и покупки на SauceDemo")
class TestSauceDemo:

    def login(self, driver, username="standard_user", password="secret_sauce"):
        with allure.step(f"Авторизация пользователя {username}"):
            driver.get(BASE_URL)
            driver.find_element(By.CSS_SELECTOR, loc.USERNAME_INPUT).send_keys(username)
            driver.find_element(By.CSS_SELECTOR, loc.PASSWORD_INPUT).send_keys(password)
            driver.find_element(By.CSS_SELECTOR, loc.LOGIN_BUTTON).click()

    @allure.title("Успешная покупка товара")
    @allure.story("Покупка")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("owner", "Alina Dementeva")
    def test_successful_purchase(self, driver):
        self.login(driver)

        with allure.step("Добавление рюкзака в корзину"):
            driver.find_element(By.CSS_SELECTOR, loc.ADD_TO_CART_BACKPACK).click()

        with allure.step("Переход в корзину"):
            driver.find_element(By.CSS_SELECTOR, loc.CART_ICON).click()

        with allure.step("Оформление заказа"):
            driver.find_element(By.CSS_SELECTOR, loc.CHECKOUT_BUTTON).click()
            driver.find_element(By.CSS_SELECTOR, loc.FIRST_NAME_INPUT).send_keys("John")
            driver.find_element(By.CSS_SELECTOR, loc.LAST_NAME_INPUT).send_keys("Doe")
            driver.find_element(By.CSS_SELECTOR, loc.ZIP_CODE_INPUT).send_keys("123456")
            driver.find_element(By.CSS_SELECTOR, loc.CONTINUE_BUTTON).click()
            driver.find_element(By.CSS_SELECTOR, loc.FINISH_BUTTON).click()

        with allure.step("Проверка успешного сообщения"):
            success_text = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, loc.SUCCESS_HEADER))
            ).text
            assert "Thank you for your order!" in success_text

    @allure.title("Очистка корзины")
    @allure.story("Корзина")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("owner", "Alina Dementeva")
    def test_cart_clearing(self, driver):
        self.login(driver)

        with allure.step("Добавление товара в корзину"):
            driver.find_element(By.CSS_SELECTOR, loc.ADD_TO_CART_BACKPACK).click()

        with allure.step("Переход в корзину"):
            driver.find_element(By.CSS_SELECTOR, loc.CART_ICON).click()

        with allure.step("Удаление товара из корзины"):
            driver.find_element(By.CSS_SELECTOR, loc.REMOVE_BACKPACK).click()

        with allure.step("Проверка, что корзина пуста"):
            badge_elements = driver.find_elements(By.CSS_SELECTOR, loc.CART_BADGE)
            assert len(badge_elements) == 0, "Корзина не пуста!"

    @allure.title("Неуспешная авторизация")
    @allure.story("Авторизация")
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("owner", "Alina Dementeva")
    def test_invalid_login(self, driver):
        driver.get(BASE_URL)

        with allure.step("Ввод неверных учетных данных"):
            driver.find_element(By.CSS_SELECTOR, loc.USERNAME_INPUT).send_keys("invalid_user")
            driver.find_element(By.CSS_SELECTOR, loc.PASSWORD_INPUT).send_keys("wrong_password")
            driver.find_element(By.CSS_SELECTOR, loc.LOGIN_BUTTON).click()

        with allure.step("Проверка сообщения об ошибке"):
            error_msg = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, loc.ERROR_MESSAGE))
            ).text
            assert "Username and password do not match" in error_msg