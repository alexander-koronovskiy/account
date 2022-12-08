from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import yaml
import json
from time import sleep


def main():
    # wd activation
    driver = webdriver.Safari(executable_path='/usr/bin/safaridriver')
    base_url = 'https://bg.alfabank.ru'
    login = base_url + '/auth/realms/farzoom-prod/account'
    tasks = base_url + '/tasks'

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
    email = driver.find_element(By.ID, 'username')
    email.send_keys(username)
    passwd = driver.find_element(By.ID, 'password')
    passwd.send_keys(_secret_key)
    driver.find_element(By.ID, 'kc-login').click()
    sleep(3)

    # redirect
    driver.get(tasks)
    sleep(3)
    driver.find_element(By.CLASS_NAME, 'btn-options__link').click()
    sleep(3)
    driver.find_element(By.CLASS_NAME, 'modal-menu__item').click()
    sleep(3)

    # fill the forms
    driver\
        .find_element(By.CLASS_NAME, 'fzp-company__autocomplete')\
        .send_keys(new_task['org_inn'])
    sleep(3)
    driver \
        .find_element(By.CLASS_NAME, 'suggestions-container') \
        .click()
    Select(driver.find_element(By.XPATH, '//select[@ng-model="model.data.bankGuaranteeTypeRefId"]')) \
        .select_by_visible_text('Обеспечение заявки на участие в торгах')
    sleep(3)

    # close
    print(driver.page_source)
    driver.close()


if __name__ == "__main__":
    main()
