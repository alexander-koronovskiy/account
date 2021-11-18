from selenium import webdriver
from selenium.webdriver.common.by import By
import yaml
from time import sleep


def main():
    # wd activation
    driver = webdriver.Safari(executable_path='/usr/bin/safaridriver')
    base_url = 'https://bg.alfabank.ru'
    login = base_url + '/auth/realms/farzoom-prod/account'
    driver.get(login)

    # yml data extract
    a_yaml_file = open('config.yml')
    config_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
    username = config_file['USER_ACCESS_KEY']
    _secret_key = config_file['USER_SECRET_KEY']

    # login
    email = driver.find_element(By.ID, 'username')
    email.send_keys(username)
    passwd = driver.find_element(By.ID, 'password')
    passwd.send_keys(_secret_key)

    # submit
    btn = driver.find_element(By.ID, 'kc-login')
    btn.click()

    # redirect
    sleep(5)
    tasks = base_url + '/tasks'
    driver.get(tasks)

    # close
    sleep(10)
    driver.close()


if __name__ == "__main__":
    main()
