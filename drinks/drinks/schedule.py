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







def chooseMonthDay(month, day, year):
    # print("monthToNum(month): ", monthToNum(month))
    # print("day: ", day)
    # print("year: ", year)

    # adjust the input month, day to previous day as the webpage
    # wrongly added 1 day after search.

    # On Sep 23 2023, the web page is correct. Therefore the if-else below commented.
    # if day == 1:
    #     #inputDate = datetime.date(day=1, month=10, year=2023)
    #     inputDate = date(year, monthToNum(month), 1)
    #     dateToUse = inputDate + timedelta(days=-1)
    #     monthToUse = dateToUse.month
    #     dayToUse = dateToUse.day
    # else:
    #     monthToUse = monthToNum(month)
    #     dayToUse = day - 1

    monthToUse = monthToNum(month)
    dayToUse = day

    # print("monthToUse", monthToUse)
    # print("dayToUse", dayToUse)

    calendar = driver.find_elements("xpath", "//*[@id='outbound-datepicker-controller-div']/span/button/i")
    if calendar:
        a.move_to_element(calendar[0]).click().perform()
        time.sleep(0.5)
                                            
        monthShown = driver.find_elements("xpath", "//*[starts-with(@id, 'datepicker') and contains(@id, '-title')]")
        if monthShown:
            # print("monthShown[0].get_attribute('id') is ", monthShown[0].get_attribute("id"))
            datepicker = monthShown[0].get_attribute("id")[0:len(monthShown[0].get_attribute("id"))-5]
            # print("datepicker", datepicker)
            # print("monthShown is: ", monthShown[0].text)
            if monthToNum(monthShown[0].text) < monthToUse:
                clicks = monthToUse - monthToNum(monthShown[0].text)
            elif monthToNum(monthShown[0].text) > monthToUse:
                clicks = 12 + monthToUse - monthToNum(monthShown[0].text)
            else:
                clicks = 0

            print("clicks: ", clicks)
            nextMonth = driver.find_elements("xpath", "//*[@id='outbound-datepicker-controller-div']/ul/li/div/table/thead/tr[1]/th[3]/button/i")
            if nextMonth:
                for i in range(0, clicks):
                    nextMonth[0].click()

                if chooseDay(dayToUse, datepicker):
                    return True

    return False


def chooseDay(day, datepicker):
    startOfMonth = False

    for i in range(0, 42):
        # path = "//*[starts-with(@id, 'datepicker') and contains(@id, '-" + str(i) + "')]"
        path = "//*[@id='" + datepicker + str(i) + "']"
        # print("path: ", path)
        dayNum = driver.find_elements("xpath", path)
                                              
        if dayNum:
            index = 0
            
            if dayNum[index].text == "01":
                startOfMonth = True
            
            if startOfMonth and int(dayNum[index].text) == day:
                dayNum[index].click()
                return True
        else:
            print("dayNum not found")
            
    return False
            

def monthToNum(month):
    month3 = month[0:3]
    if month3 == "Jan":
        return 1
    elif month3 == "Feb":
        return 2
    elif month3 == "Mar":
        return 3
    elif month3 == "Apr":
        return 4
    elif month3 == "May":
        return 5
    elif month3 == "Jun":
        return 6
    elif month3 == "Jul":
        return 7
    elif month3 == "Aug":
        return 8
    elif month3 == "Sep":
        return 9
    elif month3 == "Oct":
        return 10
    elif month3 == "Nov":
        return 11
    elif month3 == "Dec":
        return 12
    else:
        return 0
        

def LAXTo(airport, month, day, year):

    driver.get("https://tracker.flightview.com/customersetup/Laxairport/internettimetable/")
    time.sleep(2)

    driver.switch_to.frame("ifrViewport")

    oneWay = driver.find_elements("xpath", "//*[@id='rt-one-way-option']")
                                            
    if oneWay:
        time.sleep(0.5)
        oneWay[1].click()

        toAirportInput = driver.find_elements("xpath", "//*[@id='flight-finded-destination-autocomplete-input']")
        if toAirportInput:
            toAirportInput[0].send_keys(airport)
            time.sleep(0.5)
            toAirportInput[0].send_keys(Keys.RETURN)
            
            if chooseMonthDay(month, day, year):
                nonStop = driver.find_elements("xpath", "//*[@id='non-stop-check-non']")
                if nonStop:
                    nonStop[0].click()
                    search = driver.find_elements("xpath", "//*[@id='search-button']")
                    if search:
                        search[0].click()
                        time.sleep(2)

                        noOfDirect = driver.find_elements("xpath", "//*[@id='tab-heading-outbound-direct-count']")
                        if noOfDirect:
                            text = noOfDirect[0].text.strip()
                            print("noOfDirect[0].text: ", text)
                            print("text[1:len(text)-1]: ", text[1:len(text)-1])

                            if len(text) > 0:
                                directCount = int(text[1:len(text)-1])

                                for i in range(0, directCount):
                                    airline = driver.find_elements("xpath", "//*[@id='flight-outbound-directs']/div[" + str(i+2) + "]/div[1]/div/div[2]/div[1]/div[1]")
                                    nonStop = driver.find_elements("xpath", "//*[@id='flight-outbound-directs']/div[" + str(i+2) + "]/div[1]/div/div[2]/div[2]/div[1]/span")                           
                                    departs = driver.find_elements("xpath", "//*[@id='flight-outbound-directs']/div[" + str(i+2) + "]/div[1]/div/div[2]/div[1]/div[6]")
                                    arrivesPlus = driver.find_elements("xpath", "//*[@id='flight-outbound-directs']/div[" + str(i+2) + "]/div[1]/div/div[2]/div[1]/div[7]")
                                    print("airline: ", airline[0].text)
                                    print("departs: ", departs[0].text)
                                    print("arrivesPlus: ", arrivesPlus[0].text)

                                    if (nonStop[0].text == "Non-Stop"):

                                        text = arrivesPlus[0].text
                                        textRight = text[len(text)-4:]
                                        if textRight == "(+1)":
                                            arrives = text[0:len(text)-5]
                                            arriveDateChg = 1
                                        else:
                                            arrives = text
                                            arriveDateChg = 0

                                        month00 = "{:02d}".format(monthToNum(month))
                                        day00 = "{:02d}".format(day)

                                        myJson = {     
                                                    "fromAirport": "LAX",
                                                    "toAirport": airport,
                                                    "date": str(year) + "-" + month00 + "-" + day00,
                                                    "airline": airline[0].text,
                                                    "departs": departs[0].text,
                                                    "arrives": arrives,
                                                    "arriveDateChg": arriveDateChg
                                                }
                                        requests.post("http://127.0.0.1:8000/flight/", json = myJson)


    else:
        print("oneWay not found")

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
    a = ActionChains(driver)


    UtahAirport = [ "CDC", "CNY", "OGD", "PVU", "SGU", "SLC" ]

    # for airport in UtahAirport:
    #     LAXTo(airport, "Nov", 2, 2023)

    for day in range(1, 2):
        LAXTo("DEN", "Feb", day, 2024)

    # LAXTo("DEN", "Feb", 6, 2024)
