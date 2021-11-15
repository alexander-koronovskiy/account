from selenium import webdriver
import time


def main():
    driver = webdriver.Safari(executable_path='/usr/bin/safaridriver')
    url = 'https://bg.alfabank.ru'

    driver.get('https://accounts.google.com')
    email = driver.find_element_by_id('identifierId')
    email.send_keys('hahaha')
    next = driver.find_element_by_id('identifierNext')
    next.click()
    time.sleep(5)  # думал, может страница не успевает появиться, нет не в этом причина:(
    passwd = driver.find_elements_by_name('password')
    passwd.send_keys('*bzZ%tEDsFF6PKBP')


if __name__ == "__main__":
    main()
