from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from parse_yaml import cred_data


class PythonLinkedin:

    def __init__(self):
        self.__cred_data = cred_data
        self.__driver = webdriver.Chrome('chromedriver.exe')

    @property
    def driver(self):
        return self.__driver

    def account_login(self):
        """
        Code to login into linkedin home.
        :return: None
        """
        self.driver.get(self.__cred_data.login)
        username = self.driver.find_element(by=By.XPATH, value='//*[@id="session_key"]')
        password = self.driver.find_element(by=By.XPATH, value='//*[@id="session_password"]')
        username.send_keys(self.__cred_data.username)
        password.send_keys(self.__cred_data.password)
        login_btn = self.driver.find_element(by=By.XPATH, value="//button[@class='sign-in-form__submit-button']")
        login_btn.click()

    def account_logout(self):
        """
        Logout of the account.
        :return: None
        """
        self.driver.execute_script("window.open('');")
        sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(self.__cred_data.logout)
        sleep(3)

    def get_search_url(self, role):
        """
        Search by the keyword and return the search url.
        :param role: Job Designation.
        :return: Search result URL.
        """
        search_bar = self.driver.find_element(by=By.XPATH, value='//*[@id="global-nav-typeahead"]/input')
        search_bar.send_keys(role)
        search_bar.send_keys(Keys.ENTER)
        sleep(5)
        search_by_people = self.driver.find_element(by=By.XPATH, value='//button[text()="People"]')
        search_by_people.click()
        sleep(5)
        return self.driver.current_url

    def close_driver(self):
        """
        Quit Chrome Browser.
        :return: None
        """
        self.driver.quit()


pl = PythonLinkedin()
pl.account_login()
sleep(5)
pl.account_logout()
sleep(2)
pl.close_driver()


