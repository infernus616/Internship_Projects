import pandas as pd
import numpy as np
import socket
import time
from contextlib import closing
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import datetime
import pychrome
from pymongo import MongoClient
from selenium.webdriver.common.action_chains import ActionChains


class myClass:
    def __init__(self,version):
        self.hostname = "one.one.one.one"
        # self.loop_connected()
        self.options = webdriver.ChromeOptions()
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.22 Safari/537.36'
        self.port_number = self.find_free_port()
        self.port_url = "--remote-debugging-port=" + str(self.port_number)
        self.options.add_argument(f'user-agent={self.user_agent}')
        self.options.add_argument(self.port_url)
        self.options.add_argument("--disable-renderer-backgrounding")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-gpu")
        # self.options.add_argument("--disable-features=NetworkService")
        self.options.add_argument("--disable-features=VizDisplayCompositor")
        self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=self.options
        )
        self.url = "http://localhost:" + str(self.port_number)
        self.dev_tools = pychrome.Browser(url=self.url)
        self.tab = self.dev_tools.list_tab()[0]
        self.tab.start()
        # self.driver.get("https://www.google.co.in")  # remove once done
        self.driver.get("https://www.google.com")
    def is_connected(self):
        try:
            host = socket.gethostbyname(self.hostname)
            s = socket.create_connection((host, 80), 2)
            s.close()
            return True
        except:
            return False

    def loop_connected(self):
        if self.is_connected():
            return True
        else:
            print("Internet Disabled")
            time.sleep(100)
            self.loop_connected()

    def find_free_port(self):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(("", 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

    def set_location(self, latitude, longitude, url):
        self.loop_connected()
        self.driver.get("https://www.google.com/search?q=a")
        time.sleep(3)
        self.tab.call_method("Network.enable", _timeout=20)
        self.tab.call_method("Browser.grantPermissions", permissions=["geolocation"])
        self.tab.call_method(
            "Emulation.setGeolocationOverride",
            latitude=latitude,
            longitude=longitude,
            accuracy=100,
        )
        time.sleep(20)
        try:
            self.bodyText = self.driver.find_element_by_tag_name("body").text
            if "Use precise location" in self.bodyText:
                self.driver.find_element_by_xpath(
                    "//a[text()='Use precise location']"
                ).click()
            else:
                self.driver.find_element_by_xpath("//a[text()='Update location']").click()
            time.sleep(3)
        except NoSuchElementException:
            self.loop_connected()
            self.driver.refresh()
            time.sleep(5)
            self.bodyText = self.driver.find_element_by_tag_name("body").text
            if "Use precise location" in self.bodyText:
                self.driver.find_element_by_xpath(
                    "//a[text()='Use precise location']"
                ).click()
            else:
                self.driver.find_element_by_xpath("//a[text()='Update location']").click()
            time.sleep(3)
        self.driver.get(str(url))

    # def change_language_settings(self, language):
    #     self.xpath = "//a[text()='" + str(language) + "']"
    #     self.driver.find_element_by_xpath(self.xpath).click()
    def change_language_settings(self,language):
        language_link = 'https://www.google.com/?hl='+str(language)
        self.driver.get(language_link)

    def separate_alphabets(self, letter):
        self.search_field = self.driver.find_element_by_name("q")
        self.autocomplete_list_of_a_letter = []
        self.letter = letter
        self.search_field.send_keys(str(self.letter))
        time.sleep(1.25)  # do not forget to change it
        for self.loop in range(1, 11):
            try:
                self.li_items = self.driver.find_element_by_xpath(
                    "//*/ul/li[%d]/div/div[2]/div[1]" % (self.loop)
                ).text
                self.autocomplete_list_of_a_letter.append(self.li_items)
            except NoSuchElementException:
                time.sleep(2)
                try:
                    self.li_items = self.driver.find_element_by_xpath(
                        "//*/ul/li[%d]/div/div[2]/div[1]" % (self.loop)
                    ).text
                    self.autocomplete_list_of_a_letter.append(self.li_items)
                except NoSuchElementException:
                    for self.inner_loop in range(self.loop - 1, 10):
                        self.autocomplete_list_of_a_letter.append(None)
                    break
        self.driver.find_element_by_name("q").clear()
        return self.autocomplete_list_of_a_letter

    def retrieving_alphabets(self, alphabets):
        self.alphabets = alphabets
        self.json_letters = {}
        self.search_field = self.driver.find_element_by_name("q")
        for self.i in range(len(self.alphabets)):
            self.json_letters[self.alphabets[self.i]] = self.separate_alphabets(
                self.alphabets[self.i]
            )
        return self.json_letters
