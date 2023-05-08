import pygsheets
import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# authorization
gc = pygsheets.authorize(service_file='key.json')

# Create empty dataframe
df = pd.DataFrame()

# Create a column
df['Company'] = []
df['Name'] = []
df['Link'] = []

# open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sheet = gc.open_by_url(
    'https://docs.google.com/spreadsheets/d/1AqJie8U_w7Gd3TBUyqYmR23RZ-eHBylwZRrhhh5cFDg/edit#gid=0')

# select the first sheet
# scrapedSheet = sheet[4]

# update the first sheet with df, starting at cell B2.
# scrapedSheet.set_dataframe(df,(1,1))

companies = []
names = []
links = []

s_companies = []
s_names = []
s_links = []


options = webdriver.ChromeOptions()
options.add_argument("--incognito")
# options.add_argument("--headless")
options.add_argument('log-level=3')
browser = webdriver.Chrome("chromedriver.exe", options=options)
browser.set_window_size(1920, 1080)
browser.maximize_window()


def get_all_outreach():
    for person in range(6, 13):
        for line in range(2, 5):
            print(sheet[person].cell(f"A{line}").value)
            if ((sheet[person].cell(f"A{line}").value != '') and (sheet[person].cell(f"B{line}").value != '') and (sheet[person].cell(f"C{line}").value != '')):
                companies.append(sheet[person].cell(f"A{line}").value)
                names.append(sheet[person].cell(f"B{line}").value)
                links.append(sheet[person].cell(f"C{line}").value)

    print(companies)
    print(names)
    print(links)

    df['Company'] = companies
    df['Name'] = names
    df['Link'] = links


def write_total_outreach():
    total_sheet = sheet[5]
    total_sheet.set_dataframe(df, (1, 1))


def parse_headline(headline, index):
    headline = headline.text.split(" ")
    for j in range(len(headline)):
        headline[j] = headline[j].upper()
    if (("CAMPUS" not in headline) and ("EARLY" not in headline) and ("STUDENT" not in headline) and ("UNIVERSITY") not in headline):
        print(headline)
    name = browser.find_element(
        "xpath", f'/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[{index}]/div/div/div[2]/div[1]/div[1]/div/span[1]/span/a/span/span[1]').text
    link = browser.find_element(
        "xpath", f'/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[{index}]/div/div/div[2]/div[1]/div[1]/div/span[1]/span/a').get_attribute("href")
    if ((name not in names) and (link not in links)):
        print(name)
        for word in range(len(headline)):
            if ((headline[word] == "AT") or (headline[word] == "@")):
                s_companies.append(headline[word+1])
                s_names.append(name)
                s_links.append(link)
                break


def scrape_recruiters(email,pw):

    browser.get("https://www.linkedin.com/in/calvin-zheng-a44554275/")
    time.sleep(2)
    browser.find_element(
        "xpath", '//*[@id="public_profile_contextual-sign-in"]/div/section/main/div/div/div[1]/button').click()

    browser.find_element(
        "id", 'public_profile_contextual-sign-in_sign-in-modal_session_key').send_keys(email)

    browser.find_element(
        "id", 'public_profile_contextual-sign-in_sign-in-modal_session_password').send_keys(pw)

    browser.find_element(
        "xpath", '//*[@id="public_profile_contextual-sign-in_sign-in-modal"]/div/section/main/div/form/div[2]/button').click()

    time.sleep(15)

    browser.find_element(
        "xpath", '//*[@id="global-nav-typeahead"]/input').send_keys(f"Campus Recruiter{Keys.RETURN}")
    time.sleep(5)

    browser.find_element(
        "xpath", '//*[@id="search-reusables__filters-bar"]/ul/li[2]/button').click()
    time.sleep(3)

    for page in range(2,10):
        for i in range(1, 11):
            headline = browser.find_elements(
                "xpath", f"/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[{i}]/div/div/div[2]/div[1]/div[2]/div[1]")
            for h in headline:
                parse_headline(h, i)
        main_window = browser.current_window_handle

        # 
        # 
        browser.execute_script(f'window.open("https://www.linkedin.com/search/results/people/?keywords=Campus%20Recruiter&origin=SWITCH_SEARCH_VERTICAL&page={page}","_blank");')
        # browser.get(f"https://www.linkedin.com/search/results/people/?keywords=Campus%20Recruiter&origin=SWITCH_SEARCH_VERTICAL&page={page}")
        time.sleep(3)
        browser.switch_to.window(browser.window_handles[page-1])
        # browser.switch_to.window(main_window)
        time.sleep(1)
        # 
        # 

        
def write_scraped_recruiters():
    df['Name'] = s_names
    df['Company'] = s_companies
    df['Link'] = s_links
    total_sheet = sheet[4]
    total_sheet.set_dataframe(df, (1, 1))

# get_all_outreach()
# write_total_outreach()
scrape_recruiters("","")
write_scraped_recruiters()

print(s_names)
print("")
print(s_links)
print("")
print(s_companies)
