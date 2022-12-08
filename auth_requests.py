from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import yaml
import json
from time import sleep


def main():
    # wd activation
    driver = webdriver.Safari(executable_path='/usr/bin/safaridriver')
    base_url = 'https://platonus.nnsoft.kz'
    login = base_url + '/template.html#/welcome'
    tasks = base_url + '/'

    # login data extract
    a_yaml_file = open('config.yml')
    config_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
    username = config_file['USER_ACCESS_KEY']
    _secret_key = config_file['USER_SECRET_KEY']

    # forms data extract
    example_path = open('task_0.json')
    new_task = json.load(example_path)

    # login
    driver.get(login)
    email = driver.find_element(By.ID, 'iin_input')
    email.send_keys(username)
    passwd = driver.find_element(By.ID, 'pass_input')
    passwd.send_keys(_secret_key)
    driver.find_element(By.ID, 'pass-status').click()
    sleep(5)

    # close
    print(driver.page_source)
    driver.close()


if __name__ == "__main__":
    main()
