import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def test_login_page_is_displayed(self):
        """
        Open website and check if login page is rendered
        and 'Login' is shown as page title
        """
        self.browser.get("http://localhost:8000")
        self.assertIn("Login", self.browser.title)

    def test_user_can_open_register_page(self):
        """
        Check if user can go from login page to register
        """
        self.browser.get("http://localhost:8000")
        register_button = self.browser.find_element_by_tag_name("a")
        register_button.click()
        time.sleep(1)

        self.assertIn("Create an account", self.browser.title)


    
    def tearDown(self):
        self.browser.quit()


if __name__ == "__main__":
    unittest.main()
