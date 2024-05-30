from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time 
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta, date
import requests
from drinks.schedule import monthToNum




def searchFlight(fromAirport, toAirport, departDate, driver):
    driver.get("https://www.flightsfrom.com/" + fromAirport + "-" + toAirport)

    a = ActionChains(driver)

    flightArray = []

    calendarMonth = driver.find_elements("xpath", "//*[@id='color-calendar']/div/div[2]/div[2]/span[1]")
    if calendarMonth:
        monthLabel = calendarMonth[0].text
        print("monthLabel: ", monthLabel)

        if monthToNum(monthLabel) < departDate.month:
            clicks = departDate.month - monthToNum(monthLabel)
        elif monthToNum(monthLabel) > departDate.month:
            clicks = 12 + departDate.month - monthToNum(monthLabel)
        else:
            clicks = 0

        print("clicks: ", clicks)

        nextMonth = driver.find_elements("xpath", "//*[@id='color-calendar']/div/div[2]/div[3]/div")
        if nextMonth:
            a.move_to_element(nextMonth[0]).perform()
            print("move to next month button")
            time.sleep(1.0)
            driver.execute_script("window.scrollBy(0, 500);", "")
            print("scroll up")
            time.sleep(1.0)

            for i in range(0, clicks):
                a.move_to_element(nextMonth[0]).perform()
                print("move to next month button")
                time.sleep(0.5)
                nextMonth[0].click()
                print("click on next month")
                time.sleep(1.0)

        startOfMonth = False
        i = 1
        while i < 43:
            print("i: ", i)

            # if startOfMonth == False:
            dayNum = driver.find_elements("xpath", "//*[@id='color-calendar']/div/div[3]/div[2]/div[" + str(i) + "]")
            
            # if not dayNum:
            #     dayNum = driver.find_elements("xpath", "//*[@id='color-calendar']/div/div[3]/div[2]/div[" + str(i) + "]/span")

            if dayNum:
                if dayNum[0].text == "1":
                    startOfMonth = True
                    print("i: ", i)
                    print("Start month = True")

                if startOfMonth and int(dayNum[0].text) == departDate.day:
                    # a.move_to_element(dayNum[0]).perform()
                    # time.sleep(1)
                    # driver.execute_script("window.scrollBy(0, 100);", "")
                    # time.sleep(1)
                    a.move_to_element(dayNum[0]).click().perform()
                    print("click on the day")

                    continueLoad = True
                    j = 1
                    while continueLoad:
                        fromToTime = driver.find_elements("xpath", "//*[@id='calendarPopup_all']/div[1]/table/tbody/tr[" + str(j) + "]/td[1]/a")
                        if fromToTime:
                            dashIndex = fromToTime[0].text.find("-")
                            if dashIndex != -1:
                                fromTime24 = fromToTime[0].text[0:dashIndex]
                                dFrom = datetime.strptime(fromTime24, "%H:%M")
                                fromTime = dFrom.strftime("%I:%M %p")

                                toTime24 = fromToTime[0].text[dashIndex+1:]
                                dTo = datetime.strptime(toTime24, "%H:%M")
                                toTime = dTo.strftime("%I:%M %p")

                                if dTo < dFrom:
                                    arriveDateChg = 1
                                else:
                                    arriveDateChg = 0

                                airline = driver.find_elements("xpath", "//*[@id='calendarPopup_all']/div[1]/table/tbody/tr[" + str(j) + "]/td[2]/a/span[2]")[0].text
                        
                                print("y is: ", departDate.year)
                                print("m is: ", departDate.month)
                                print("d is: ", departDate.day)

                                departDateStr = str(departDate.year) + "-" + ("0" + str(departDate.month))[-2:] + "-" + ("0" + str(departDate.day))[-2:]

                                aFlight = {
                                    "fromAirport": fromAirport,
                                    "toAirport": toAirport,
                                    "date": departDateStr,
                                    "airline": airline,
                                    "departs": fromTime,
                                    "arrives": toTime,
                                    "arriveDateChg": arriveDateChg
                                }

                                flightArray.append(aFlight)

                                print("Flight: ", fromTime, " ", toTime, " ", airline, " ", arriveDateChg)
                                j = j+1
                        else:
                            continueLoad = False
                
                    # Force to end
                    i = 43

            i = i + 1
    return flightArray


def multiSearch(fromAirportList, toAirportList, departDateFrom, departDateTo):

    service = Service()
    chrome_options = Options()
    #The below option make opened Chrome detached from Python program, 
    #Chrome will keep open even if Python program end (suppose not explictly close it
    #in program)
    #Or, if you want to auto-close Chrome upon Python program end, comment this out.
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(3) # seconds
    #a = ActionChains(driver)

    flightArray = []

    for fromAirport in fromAirportList:
        for toAirport in toAirportList:
            dateUsed = departDateFrom
            while dateUsed <= departDateTo:
                print("fromAirport is: ", fromAirport)
                print("toAirport is: ", toAirport)
                flightArray = flightArray + searchFlight(fromAirport, toAirport, dateUsed, driver)
                dateUsed = dateUsed + timedelta(days=1)

    driver.quit()
    return flightArray

# The below if is used to prevent these codes being run when this file is imported by other .py program
if __name__ == "__main__":

    service = Service()
    chrome_options = Options()
    #The below option make opened Chrome detached from Python program, 
    #Chrome will keep open even if Python program end (suppose not explictly close it
    #in program)
    #Or, if you want to auto-close Chrome upon Python program end, comment this out.
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(3) # seconds
    #a = ActionChains(driver)

    departDate = date(2023, 9, 30)

    searchFlight("LAX", "IAD", departDate, driver)