from selenium import webdriver                              # webdriver for controlling chrome
from selenium.webdriver.common.by import By                 # for by search functions in selenium
from selenium.webdriver.chrome.service import Service       # for making a service type obj
from time import sleep                                      # for pausing execution
import requests                                             # for retrieving the page
from bs4 import BeautifulSoup                               # for parsing the page html
import json                                                 # for writing extracted data to json file
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import select


# starting chrome through webdriver, accessing yahoo finance and then S&P500 page
path = Service("E:\selenium_chrome_driver\chromedriver")
chrome = webdriver.Chrome(service = path)
chrome.get(url = "https://finance.yahoo.com/")
snp500 = chrome.find_element(by = By.PARTIAL_LINK_TEXT, value = "S&P")
snp500.click()
sleep(15)


# retrieving the page, checking that everything's ok, then grabbing the table from the html
url = chrome.current_url
response = requests.get(url = url)
if int(response.status_code) != 200:
    print('Error:', response.status_code)
    quit()
soup1 = BeautifulSoup(response.content, 'html.parser')
main_table = soup1.find_all('table', {'class':'W(100%)'})


# separating rows of both tables
table1 = main_table[0].find_all('tr', {'class':'Bxz(bb)'})
table2 = main_table[1].find_all('tr', {'class':'Bxz(bb)'})


# separating headings and values and then storing them as key-value pairs
table1_headings = []
table1_values = []
table2_headings = []
table2_values = []
table = {}

for i in range(len(table1)):
    table1_headings.append(table1[i].find_all('td', {'class':'C($primaryColor) W(51%)'}))
    table1_values.append(table1[i].find_all('td', {'class':'Ta(end) Fw(600) Lh(14px)'}))
    table2_headings.append(table2[i].find_all('td', {'class':'C($primaryColor) W(51%)'}))
    table2_values.append(table2[i].find_all('td', {'class':'Ta(end) Fw(600) Lh(14px)'}))
    table[table1_headings[i][0].get_text()] = table1_values[i][0].get_text()
    table[table2_headings[i][0].get_text()] = table2_values[i][0].get_text()

print(table)

# storing data in file
with open('summary.txt', 'w') as out1:
    json.dump(table, out1)


# Second task
snp500history = chrome.find_element(by = By.LINK_TEXT, value = "Historical Data")
snp500history.click()
sleep(5)
# retrieving the page, checking that everything's ok, then grabbing the needed contents from the html
url2 = chrome.current_url
url2 = 'https://finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC'
response2 = requests.get(url = url2, headers={'User-Agent': 'Custom'}
                         )
if int(response2.status_code) != 200:
    print('Error:', response2.status_code)
    quit()
soup2 = BeautifulSoup(response2.content, 'html.parser')
duration = soup2.find_all('div', {'class':'Bgc($lv1BgColor) Bdrs(3px) P(10px)'})
t = duration[0].find_all('span', {'class':'C($linkColor) Fz(14px)'})
print(t[0].get_text())


table = chrome.find_elements(by = By.XPATH, value = '//table[contains(@class,"W(100%)")]')
chrome.implicitly_wait(15)

for i in range(len(table)):
    print(table[i].text)
    print('\n\n')

chrome.quit()