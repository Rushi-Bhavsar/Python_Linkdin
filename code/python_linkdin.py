from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from parse_yaml import cred_data

# LOGIN = 'https://www.linkedin.com/home'
# LOGOUT = 'https://www.linkedin.com/m/logout/'


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
        login_btn = self.driver.find_element(by=By.XPATH, value="//*[@type='submit']")
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
        current_search_url = self.driver.current_url
        self.create_process_page(current_search_url)
        return self.driver.current_url

    def create_process_page(self, current_search_url):
        for pageNo in range(1, 3):
            print("*" * 40)
            print(f"Processing Page {pageNo} records.")
            if pageNo > 1:
                if 'page=' in current_search_url:
                    current_search_url = current_search_url.replace(f'page={pageNo - 1}', f'page={pageNo}')
                else:
                    current_search_url = current_search_url.replace('=SWITCH_SEARCH_VERTICAL&',
                                                                    f'=SWITCH_SEARCH_VERTICAL&page={pageNo}&')
                self.driver.get(current_search_url)
                sleep(2)
            self.process_page()

    def process_page(self):
        ul_element = self.driver.find_elements(by=By.CLASS_NAME, value='reusable-search__result-container')
        connection_information = {}
        page_info = []
        for item in ul_element:
            try:
                connect_btn = item.find_element(by=By.TAG_NAME, value='button')
            except NoSuchElementException:
                print(f"Connect Button not found. skipping record")
                continue
            btn_value = connect_btn.find_element(by=By.TAG_NAME, value='span').text
            if btn_value != 'Connect':
                continue
            try:
                image = item.find_element(by=By.TAG_NAME, value='img')
            except NoSuchElementException:
                name = item.find_element(by=By.CLASS_NAME, value='visually-hidden')
                print(f"Name: {name.text}")
                print("Image is not present.")
                image = ''
                connection_information['name'] = name.text
                connection_information['image'] = image
            if image:
                image_link = image.get_attribute('src')
                name = image.get_attribute('alt')
                print(f"Name: {name}")
                print(f'Image Link: {image_link}')
                connection_information['name'] = name
                connection_information['image'] = image_link
            link = item.find_element(by=By.XPATH, value='.//div/div/div[1]/div/a').get_attribute('href')
            print(f'Link: {link.split("?")[0]}')
            skill = item.find_element(by=By.XPATH, value='.//div/div/div[2]/div[1]/div[2]/div[1]')
            print(f"Skill: {skill.text}")
            location = item.find_element(by=By.XPATH, value='.//div/div/div[2]/div[1]/div[2]/div[2]')
            print(f'Location: {location.text}')
            # print(f'Connection Button Found: {btn_value}')
            # To send connection request we need to connect_btn.click()
            try:
                info = item.find_element(by=By.XPATH, value='.//div/div/div[2]/div[2]/p')
                print(f"Info: {info.text}")
                print('-' * 50)
            except NoSuchElementException:
                print(f"No Info present.")
                info = ''
            connection_information['link'] = link
            connection_information['skill'] = skill
            connection_information['location'] = location
            connection_information['info'] = info
            page_info.append(connection_information)
        # We can save Connection_Information per Page into Database/File using "page_info"

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
    pl.account_logout()
    sleep(5)


driver_code()
