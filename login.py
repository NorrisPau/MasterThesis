from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

#Open Tinder using selenium
#Source: https://github.com/ifrankandrade/automation/blob/main/Tinder/en-tutorial.py
path = "/usr/local/bin/chromedriver" #path of chrome driver
service = Service(executable_path=path)
web = "https://tinder.com/" #Website to go to
driver = webdriver.Chrome(service=service)

options = Options()
options.add_experimental_option("debuggerAddress", "localhost:9222") #we indicated localhost before
driver = webdriver.Chrome(service=service, options=options)

driver.get(web) #Go to Tinder.com

