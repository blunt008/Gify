from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def test_login_page_is_displayed(self):
        self.browser.get("http://localhost:8000")
        self.assertIn("Login", self.browser.title)
    
    def tearDown(self):
        self.browser.quit()


if __name__ == "__main__":
    unittest.main()
