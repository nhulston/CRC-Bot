# Fill in CRC_USERNAME, CRC_PASSWORD, DRIVER_PATH, and BROWSER_PATH. The driver can be downloaded here: https://chromedriver.chromium.org/downloads

import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DRIVER_PATH = "C:\Program Files (x86)\ChromeDriver\chromedriver.exe"
BROWSER_PATH = "C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\\brave.exe" #You can use Google Chrome also
CRC_USERNAME = "TODO"
CRC_PASSWORD = "TODO"


LINK = "https://mycrc.gatech.edu/Program/GetProgramDetails?courseId=f35f5e43-00fd-4257-b31a-25bef19b13e5" \
       "&semesterId=6f336ff2-0847-434b-a247-6814da94f1bc "

# BeautifulSoup variables
result = requests.get(LINK)
src = result.content
soup = BeautifulSoup(src, "lxml")

# Get times available
times = []
text = soup.find_all(text=True)
for t in text:
    trimmed = t.strip()
    if len(trimmed) > 0 and trimmed[0].isdigit() and "-" in trimmed:
        times.append(trimmed)

# User input
delay = int(input("How often do you want to check the page? (~5 seconds recommended): "))
print("")
for x in range(0, len(times)):
    print(chr(x + 97) + ") " + times[x])
letter = input("\nWhat time do you want to scan for: ")
time_slot = times[ord(letter) - 97]
print("\nNow scanning time slot: " + time_slot + "\n")

# Starting loop...
while True:
    # Refresh data from the website
    result = requests.get(LINK)
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    text = soup.find_all(text=True)

    # Check if time slot is no longer listed (30 min before, no longer able to sign up)
    if time_slot not in map(str.strip, text):
        print("A spot was not found. Sorry ):")
        break

    # Get text from time slot
    for x in range(0, len(text)):
        if text[x].strip() == time_slot:
            index = x + 2
            break

    results = text[index]
    if results[0] != 'N':
        print("THERE IS A SPOT AVAILABLE!")
        options = Options()
        options.binary_location = BROWSER_PATH
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

        driver.get(LINK)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[2]/a[2]"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div["
                                                                              "4]/div/div/div/div[2]/div[2]/div["
                                                                              "3]/div/button"))).click()
        driver.implicitly_wait(10)
        driver.find_element_by_xpath("/html/body/div[5]/div[4]/div/div/div/div[3]/div[2]/div[1]/div/input")\
            .send_keys(CRC_USERNAME)
        driver.find_element_by_xpath("/html/body/div[5]/div[4]/div/div/div/div[3]/div[2]/div[2]/div/input")\
            .send_keys(CRC_PASSWORD + Keys.ENTER)

        x = 1
        while True:
            button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div["
                                                                                           "1]/div[2]/div[7]/div[" +
                                                                                 str(x) + "]/div/div/h4/small")))
            button_text = button.text
            button_text = button_text[:button_text.index("\n")]
            if button_text == time_slot:
                register_xpath = "/html/body/div[5]/div[1]/div[2]/div[7]/div[" + str(x) + "]/div/div/div/button"
                break
            else:
                x += 2

        driver.implicitly_wait(10)
        driver.find_element_by_xpath(register_xpath).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[1]/div[2]/div["
                                                                              "3]/div[1]/div/form/button"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[1]/div[2]/div["
                                                                              "3]/div/form/button"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[1]/div[2]/div["
                                                                              "5]/div/div/div[2]/div/div["
                                                                              "2]/button"))).click()
        break
    else:
        print("No spots available for " + time_slot + "...")
        time.sleep(delay)
