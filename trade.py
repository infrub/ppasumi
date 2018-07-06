#! /usr/bin/env python
# coding: utf-8

from selenium import webdriver

def login(driver, userid, password):
    useridBox = driver.find_element_by_class_name("user_id")
    useridBox.send_keys(userid)
    passwordBox = driver.find_element_by_class_name("password")
    passwordBox.send_keys(password)
    
    loginButton = driver.find_element_by_name("LoginForm")
    loginButton.click()

def main():
    print('Input the driver path: ', end='')
    chromedriver = input()
    print('Input the userID: ', end='')
    userid = input()
    print('Input the password: ', end='')
    password = input()
    
    url = "https://fx-demo.click-sec.com/neo/web/trade"
    chromedriver = "/mnt/c/Program Files (x86)/Google/Chrome/Application/chromedriver_.exe"
    driver = webdriver.Chrome(chromedriver)
    driver.get(url)
    
    login(driver, userid, password)
    
if __name__ == "__main__":
    main()