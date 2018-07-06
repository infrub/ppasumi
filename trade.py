#! /usr/bin/env python
# coding: utf-8

import time
from selenium import webdriver

def login(driver, userid, password):
    useridBox = driver.find_element_by_class_name("user_id")
    useridBox.send_keys(userid)
    passwordBox = driver.find_element_by_class_name("password")
    passwordBox.send_keys(password)
    
    loginButton = driver.find_element_by_name("LoginForm")
    loginButton.click()
    
def setup_speed_order(driver):
    speedOrderButton = driver.find_element_by_class_name("header-speed")
    speedOrderButton.click()
    window_lst = driver.window_handles
    driver.switch_to_window(window_lst[1])

def set_trade_quantity(driver, tradeQuantity):
    quantityBox = driver.find_element_by_class_name("quantity")
    quantityBox.send_keys(str(tradeQuantity))
    
def entry_bid(driver):
    bidButton = driver.find_element_by_class_name("bid-button-normal")
    bidButton.click()
    
def entry_ask(driver):
    askButton = driver.find_element_by_class_name("ask-button-normal")
    askButton.click()
    
def settle_all(driver):
    settleButton = driver.find_element_by_class_name("all-settle-button")
    settleButton.click()

def main():
    print('Input the driver path: ', end='')
    chromedriver = input()
    print('Input the userID: ', end='')
    userid = input()
    print('Input the password: ', end='')
    password = input()
    
    url = "https://fx-demo.click-sec.com/neo/web/trade"
    driver = webdriver.Chrome(chromedriver)
    driver.get(url)
    
    login(driver, userid, password)
    time.sleep(1)
    
    setup_speed_order(driver)
    time.sleep(0.5)
    
    set_trade_quantity(driver, 1)
    time.sleep(0.5)
    
    entry_bid(driver)
    time.sleep(3)

    settle_all(driver)
    time.sleep(3)
    
    entry_ask(driver)
    time.sleep(3)

    settle_all(driver)
    time.sleep(3)
    
    time.sleep(10)
    
if __name__ == "__main__":
    main()
