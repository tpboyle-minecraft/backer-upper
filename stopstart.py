

##  IMPORTS

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import sys
import time


##  LOCAL IMPORTS

import connection as conn
    # IMPORTANT: you must define this file.
    # It provides the following variables:
    #    server_id
    #    admin_username
    #    admin_password
    # These are used to login to the web panel.
    # ! >>  backup.py has some additional variables that need to be set.
    # .gitignored by default because this needs to be set up by the user.


##  CONSTANTS

click_buffer = 15   # time in seconds to buffer around clicks so
                    #   a) the page is fully loaded before
                    #   b) the page fully registers the click after


##  PUBLIC INTERFACE

def stop():
    click_panel_btn("yt1")

def start():
    click_panel_btn("yt0")


##  PRIVATE METHODS

def click_panel_btn(btn_name):
    driver = setup_driver()
    navigate_to_panel(driver)
    action_btn = driver.find_element_by_name(btn_name)
    click(action_btn)
    driver.close()

def setup_driver():
    options = webdriver.FirefoxOptions()
    options.set_headless()
    return webdriver.Firefox(firefox_options=options)

def navigate_to_panel(driver):
    login(driver)
    driver.get("https://premium.bisecthosting.com/index.php?r=server/view&id=" + str(conn.server_id))

def login(driver):
    driver.get("https://premium.bisecthosting.com/index.php?r=site/login")
    username_box = driver.find_element_by_name("LoginForm[name]")
    enter_info(username_box, conn.admin_username)
    password_box = driver.find_element_by_name("LoginForm[password]")
    enter_info(password_box, conn.admin_password)
    submit_btn = driver.find_element_by_name("yt0")
    click(submit_btn)

def enter_info(input_elem, info):
    input_elem.clear()
    input_elem.send_keys(info)

def click(btn):
    time.sleep(click_buffer)
    btn.click()
    time.sleep(click_buffer)

