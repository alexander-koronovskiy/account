import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys


@pytest.fixture(scope="class")
def driver_init(request):
    web_driver = webdriver.Safari()
    request.cls.driver = web_driver
    yield
    web_driver.close()


@pytest.mark.usefixtures("driver_init")
class BasicTest:
    pass


class Test_URL_Safari(BasicTest):
    def test_lambdatest_todo_app(self):
        self.driver.get('https://lambdatest.github.io/sample-todo-app/')
        self.driver.maximize_window()

        self.driver.find_element(By.NAME, "li1").click()
        self.driver.find_element(By.NAME, "li2").click()

        title = "Sample page - lambdatest.com"
        assert title == self.driver.title

        sample_text = "Happy Testing at LambdaTest"
        email_text_field = self.driver.find_element(By.ID, "sampletodotext")
        email_text_field.send_keys(sample_text)
        time.sleep(5)

        self.driver.find_element(By.ID, "addbutton").click()
        time.sleep(5)

        output_str = self.driver.find_element(By.NAME, "li6").text
        sys.stderr.write(output_str)

        time.sleep(2)
