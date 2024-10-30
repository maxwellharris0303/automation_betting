from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from time import sleep
import remove_text
import quickstart

FILENAME = "data.txt"
def data_save(data):
    with open(FILENAME, "a", encoding='utf-8') as file:
        file.write(data + "\n")
def clear_file():
    with open(FILENAME, 'w') as file:
        file.truncate(0)
        print("File content cleared.")

clear_file()

firefox_profile_directory = 'C:/Users/root/AppData/Roaming/Mozilla/Firefox/Profiles/bcgxfdql.default-release'
firefox_options = webdriver.FirefoxOptions()
firefox_options.profile = webdriver.FirefoxProfile(firefox_profile_directory)

url = "https://oddsjam.com/betting-tools/positive-ev"

driver = webdriver.Firefox(options=firefox_options)
driver.maximize_window()
driver.get(url)
sleep(10)
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[id=\"betting-tool-table-row\"]")))

line_rows = driver.find_elements(By.CSS_SELECTOR, "div[id=\"betting-tool-table-row\"]")
print(len(line_rows))
# line_rows = line_rows[:5]
for line_row in line_rows:
    percentage_parent = line_row.find_element(By.CSS_SELECTOR, "div[id=\"percent-cell\"]")
    percetage_elements = percentage_parent.find_elements(By.CSS_SELECTOR, "span[class=\"relative text-inherit h-fit w-fit\"]")
    percentages = []
    for percentage_element in percetage_elements:
        percentages.append(percentage_element.text)
    print(f'Percentage: {percentages}')

    rec_bet_size_parent = line_row.find_elements(By.CSS_SELECTOR, "div[class=\"flex justify-between py-2 md:py-0 lg:border-none border-t border-t-brand-gray-4 col-span-2 h-full justify-center md:col-span-1\"]")[1]
    rec_bet_size_elements = rec_bet_size_parent.find_elements(By.CSS_SELECTOR, "span[class=\"relative text-inherit h-fit w-fit\"]")
    rec_bet_sizes = []
    for rec_bet_size_element in rec_bet_size_elements:
        rec_bet_sizes.append(rec_bet_size_element.text)
    print(f'Rec Bet Size: {rec_bet_sizes}')

    event_parent = line_row.find_element(By.CSS_SELECTOR, "div[class=\"flex justify-between py-2 md:py-0 lg:border-none border-t border-t-brand-gray-4 col-span-2 md:col-span-3\"]")
    tags = event_parent.find_elements(By.TAG_NAME, "p")
    event = tags[0].text
    variant = tags[1].text
    print(f'Event: {event}')
    print(f'Variant: {variant}')

    market = line_row.find_element(By.CSS_SELECTOR, "div[id=\"market-cell\"]").text
    print(f'Market: {market}')

    parent_elements = line_row.find_elements(By.CSS_SELECTOR, "div[class=\"grid items-center py-1 gap-2 -mx-4 rounded-md border border-brand-green-2 bg-[#324e1c4d] px-4 shadow-md md:mx-0 md:px-0 col-span-2 md:col-span-6 lg:px-1\"]")
    # print(len(parent_elements))
    bets = []
    best_odds = []
    sportbooks_array = []
    for parent_element in parent_elements:
        bet = parent_element.find_element(By.CSS_SELECTOR, "div[class=\"flex justify-between py-2 md:py-0 lg:border-none border-t border-t-brand-gray-4 flex items-center col-span-2 md:col-span-2 lg:w-fit\"]").text
        bets.append(bet)

        odd = parent_element.find_element(By.CSS_SELECTOR, "div[class=\"h-full pl-6 md:pl-0 col-span-3 flex items-center\"]").text
        best_odds.append(odd)

        sportbooks = []
        sportbook_elements = parent_element.find_elements(By.TAG_NAME, "img")
        for sportbook in sportbook_elements:
            text = sportbook.get_attribute('alt')
            sportbooks.append(remove_text.remove_parentheses(text))

        sportbooks_array.append(sportbooks)

    print(f'Bets: {bets}')
    print(f'Best Odds: {best_odds}')
    print(f'Sportbooks: {sportbooks_array}')

    width = line_row.find_element(By.CSS_SELECTOR, "div[class=\"w-full flex justify-end md:justify-center\"]").text
    print(f'Width: {width}')

    count = len(percentages)
    index = 0
    for _ in range(count):
        data_save(percentages[index] + "\t" + rec_bet_sizes[index] + "\t" + event + "\t" + variant + "\t" + market + "\t" + bets[index] + "\t" + best_odds[index] + "\t" + ", ".join(sportbooks_array[index]) + "\t" + width)
        index += 1
    # data_save(', '.join(percentages) + "\t" + ', '.join(rec_bet_sizes) + "\t" + event + "\t" + variant + "\t" + market + "\t" + ', '.join(bets) + "\t" + ', '.join(best_odds) + "\t" + ', '.join(sportbooks) + "\t" + width)
    # data = ', '.join(percentages) + "\t" + ', '.join(rec_bet_sizes) + "\t" + event + "\t" + variant + "\t" + market + "\t" + ', '.join(bets) + "\t" + ', '.join(best_odds) + "\t" + ', '.join(sportbooks) + "\t" + width
    # quickstart.insertContactInfo(f'Sheet1!A2', data)
    print("\n")
quickstart.save_to_sheet()