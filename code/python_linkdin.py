from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
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
        Code to log in into LinkedIn home.
        @return: None
        """
        self.driver.get(self.__cred_data.login)
        username = self.driver.find_element(by=By.XPATH, value='//*[@id="session_key"]')
        password = self.driver.find_element(by=By.XPATH, value='//*[@id="session_password"]')
        username.send_keys(self.__cred_data.username)
        password.send_keys(self.__cred_data.password)
        login_btn = self.driver.find_element(by=By.XPATH, value="//button[@class='sign-in-form__submit-button']")
        login_btn.click()
        sleep(5)

    def account_logout(self):
        """
        Logout of the account.
        @return: None
        """
        self.driver.execute_script("window.open('');")
        sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(self.__cred_data.logout)
        sleep(3)

    def get_search_url(self, role):
        """
        Search by the keyword and return the search url.
        @param role: Job Designation.
        @return: Search result URL.
        """
        search_bar = self.driver.find_element(by=By.XPATH, value='//*[@id="global-nav-typeahead"]/input')
        search_bar.send_keys(role)
        search_bar.send_keys(Keys.ENTER)
        sleep(5)
        search_by_people = self.driver.find_element(by=By.XPATH, value='//button[text()="People"]')
        search_by_people.click()
        sleep(5)
        ul_element = self.driver.find_elements(by=By.XPATH, value='//*[@id="main"]/div/div/div[1]/ul/li')
        for item in ul_element:
            try:
                image = item.find_element(by=By.TAG_NAME, value='img')
            except NoSuchElementException:
                name = item.find_element(by=By.CLASS_NAME, value='visually-hidden')
                print(f"Name: {name.text}")
                print("Image is not present.")
                image = None
            if image:
                image_link = image.get_attribute('src')
                name = image.get_attribute('alt')
                print(f"Name: {name}")
                print(f'Image Link: {image_link}')
            link = item.find_element(by=By.XPATH, value='.//div/div/div[1]/div/a').get_attribute('href')
            print(f'Link: {link.split("?")[0]}')
            skill = item.find_element(by=By.XPATH, value='.//div/div/div[2]/div[1]/div[2]/div[1]')
            print(f"Skill: {skill.text}")
            location = item.find_element(by=By.XPATH, value='.//div/div/div[2]/div[1]/div[2]/div[2]')
            print(f'Location: {location.text}')
            try:
                info = item.find_element(by=By.XPATH, value='.//div/div/div[2]/div[2]/p')
                print(f"Info: {info.text}")
                print('-'*50)
            except NoSuchElementException:
                print(f"No Info present.")

        return self.driver.current_url

    def close_driver(self):
        """
        Quit Chrome Browser.
        @return: None
        """
        self.driver.quit()


def driver_code():
    pl = PythonLinkedin()
    pl.account_login()
    search_url = pl.get_search_url("Django Developer")
    print(f"Search URL: {search_url}")
    sleep(5)


driver_code()
