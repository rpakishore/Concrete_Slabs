#!/usr/bin/env python
# coding: utf-8

# Reference - 
# http://yhhuang1966.blogspot.com/2018/04/python-logging_24.html
from util import AK_log

import json, unicodedata, re, os, time

#pip install selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

class main_instance:
    homedir = os.path.expanduser('~')
    # Define log level
    # Log levels: NOTSET DEBUG INFO WARNING ERROR CRITICAL
    log = AK_log.AKLog()
    #log.basicConfig(level=log.DEBUG,format='%(asctime)s - %(levelname)s : %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    log.setLevel(10)
    
    # Selenium Definitions
    chrome_path = Service(os.path.join(homedir, r'Documents\GitHub\chromedriver.exe'))
    implicitly_wait_time = 3
    max_wait_time = 5
    
    
    # Constructor
    def __init__(self, args):
        log = self.log
        self.args = args

        try:
            self.headless = self.args.Headless
        except:
            self.headless = False

        with open(args.filename, 'r') as f:
            self.user_prop = json.load(f)

        return

    def init_chrome(self):
        #Selenium Options
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--disable-gpu')
        if self.headless:
            options.add_argument('--headless')
        options.add_argument("disable-infobars")
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        if "Chrome_Userdata_Path" in self.user_prop.keys():
            options.add_argument('--user-data-dir=' + os.path.join(self.homedir, self.user_prop["Chrome_Userdata_Path"]))
        options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(service=self.chrome_path, options=options)
        driver = self.driver
        driver.implicitly_wait(self.implicitly_wait_time) 
        size = self.driver.get_window_size()
        driver.set_window_size(size['width']/2, size['height'])
        driver.set_window_position(size['width']/2-13, 0)
        driver.execute_script('window.focus()')
        driver.execute_cdp_cmd(
            'Network.setUserAgentOverride', 
            {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'
            }
            )

        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument", 
            {
                "source": """
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined
                            })
                            """
            }
            )

        driver.execute_cdp_cmd("Network.enable", {})
        driver.execute_cdp_cmd(
            "Network.setExtraHTTPHeaders", 
            {
                "headers": {
                    "User-Agent": "browser1"
                }
            }
            )
        self.log.info("Browser started.")
        return
    
    # Desstructor
    def __del__(self):
        try:
            self.driver.close()
            self.driver.quit()
            self.log.info("Browser closed.")
        except:
            pass
        return
    
    def do_actions(self):
        log = self.log 
        return

def sanitize(filename):
    """Return a fairly safe version of the filename.

    We don't limit ourselves to ascii, because we want to keep municipality
    names, etc, but we do want to get rid of anything potentially harmful,
    and make sure we do not exceed Windows filename length limits.
    Hence a less safe blacklist, rather than a whitelist.
    """
    blacklist = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|", "\0"]
    reserved = [
        "CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5",
        "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5",
        "LPT6", "LPT7", "LPT8", "LPT9",
    ]  # Reserved words on Windows
    filename = "".join(c for c in filename if c not in blacklist)
    # Remove all charcters below code point 32
    filename = "".join(c for c in filename if 31 < ord(c))
    filename = unicodedata.normalize("NFKD", filename)
    filename = filename.rstrip(". ")  # Windows does not allow these at end
    filename = filename.strip()
    if all([x == "." for x in filename]):
        filename = "__" + filename
    if filename in reserved:
        filename = "__" + filename
    if len(filename) == 0:
        filename = "__"
    if len(filename) > 255:
        parts = re.split(r"/|\\", filename)[-1].split(".")
        if len(parts) > 1:
            ext = "." + parts.pop()
            filename = filename[:-len(ext)]
        else:
            ext = ""
        if filename == "":
            filename = "__"
        if len(ext) > 254:
            ext = ext[254:]
        maxl = 255 - len(ext)
        filename = filename[:maxl]
        filename = filename + ext
        # Re-check last character (if there was no extension)
        filename = filename.rstrip(". ")
        if len(filename) == 0:
            filename = "__"
    return filename