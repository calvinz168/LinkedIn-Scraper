import pygsheets
import pandas as pd
from selenium import webdriver
import time

#authorization
gc = pygsheets.authorize(service_file='LinkedIn Scraper\key.json')

# Create empty dataframe
df = pd.DataFrame()

# Create a column
df['Company'] = []
df['Name'] = []
df['Link'] = []

#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1AqJie8U_w7Gd3TBUyqYmR23RZ-eHBylwZRrhhh5cFDg/edit#gid=0')

#select the first sheet 
# scrapedSheet = sheet[4]

#update the first sheet with df, starting at cell B2.
# scrapedSheet.set_dataframe(df,(1,1))


def get_all_outreach():
    companies = []
    names = []
    links = []

    for person in range(6,13):
        for line in range(2,5):
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
    total_sheet.set_dataframe(df,(1,1))

def scrape_recruiters(names,links):
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    # options.add_argument("--headless")
    browser = webdriver.Chrome("chromedriver.exe", options=options)
    browser.set_window_size(1920, 1080)
    browser.maximize_window()
    browser.get("https://www.linkedin.com")
    time.sleep(5)

    # https://www.linkedin.com/in/calvin-zheng-a44554275/

    # login to linkedin
    # search with 'recruiter', tech companies
    # grab headline, if has early talent or campus, compare with existing names lists
    # add to lists
    # return
    # write to sheet
    # 


get_all_outreach()
write_total_outreach()