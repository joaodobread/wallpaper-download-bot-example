from os import path
from json import loads
from urllib.parse import urlencode
from src.utils.file_handler import FileHandler
from src.utils.files_read_mode import FileReadMode
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import TimeoutException
from selenium.webdriver.support.expected_conditions import WebElement
from time import time
from typing import List


class Bot(Chrome):
    def __init__(self, *args, **kwargs):
        self.__file_handler = FileHandler()
        super().__init__(
            executable_path=self.__file_handler.path_generator('drivers/chromedriver.exe'),
            chrome_options=self.get_driver_prefs()
        )
        self.setup_config()
 
    def get_driver_prefs(self):
        file = self.__file_handler.read_file('driver-prefs.json', FileReadMode.READ)
        driver_prefs = loads(file.read())
        options = Options()
        options.add_experimental_option('prefs', driver_prefs)
        file.close()
        return options

    def setup_config(self):
        """Setup all configurations of bot"""
        self.__params = ['orientation', 'color']
        self.__config_path = path.join(path.abspath(''), 'config.json')
        file = self.__file_handler.read_file('config.json', FileReadMode.READ)
        self.__config = loads(file.read())
        file.close()

    def url_builder(self, term: str) -> str:
        """Return a url with query params params"""
        base_url = f"https://unsplash.com/s/photos/{term}?"
        if 'params' in self.__config.keys():
            url = base_url + urlencode(self.__config['params'])
        else:
            url = base_url
        return url

    def wait_to_load(self):
        started_load_at = time()
        while self.execute_script("return document.readyState") != "complete":
            if started_load_at > self.default_delay:
                raise TimeoutException(msg="Wait time exced")

    def get_all_images(self) -> List[WebElement]:
        self.wait_to_load()
        return self.find_elements(By.CSS_SELECTOR, '[title="Download photo"]')

    def routine(self):
        images = self.get_all_images()
        print(images)

    def run(self):
        for term in self.__config['terms']:
            url = self.url_builder(term)
            self.get(url)
            self.routine()
        
        self.quit()