from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
import schedule
import time
import re



def apply_jobs_dice():
    # Initialize the driver
    driver = webdriver.Chrome()

    # Open dice.com login page
    driver.get("https://www.dice.com/dashboard/login")

    # Find the username and password input fields and enter the credentials
    print("Enter email")
    username_input = driver.find_element(By.ID,"email")
    password_input = driver.find_element(By.ID,"password")

    username_input.send_keys("sumanbcloud@gmail.com")
    password_input.send_keys("Dice1234")
    password_input.send_keys(Keys.ENTER)

    # Wait for the dashboard to load
    wait = WebDriverWait(driver, 20)

    # wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "dashboard-page-container")))
    # Wait for the page to load
    time.sleep(5)

    # Search for jobs with the keyword "Dynatrace"
    keyword = ['dynatrace consultant', 'dynatrace engineer', 'application performance monitoring', 'splunk engineer', 'devops', 'infrastructure performance monitoring']
    search_box = driver.find_element(By.XPATH, "//*[@id='typeaheadInput']")
    for key in keyword:
        search_box.send_keys(key)
        search_box.send_keys(Keys.RETURN)

        # Wait for the search results to load
        time.sleep(5)

        # Filter with jobs that are posted today
        today_button = driver.find_element(By.XPATH,"//*[@id='facets']/dhi-accordion[2]/div[2]/div/js-single-select-filter/div/div/button[2]").click()
        # last_seven_button = driver.find_element(By.XPATH,"//*[@id='facets']/dhi-accordion[2]/div[2]/div/js-single-select-filter/div/div/button[4]").click()

        # Filter with "Easy Apply" jobs only
        easy_apply_button = driver.find_element(By.XPATH,"//*[@id='singleCheckbox']/span/button/i")
        easy_apply_button.click()


        # find the select element for item view per page
        select_element = Select(driver.find_element(By.XPATH,"//*[@id='pageSize_2']"))

        # select the desired item view option
        select_element.select_by_value('100')  # change to the value of your desired option

        # wait for the page to reload with the new item view
        time.sleep(3)


        links = driver.find_elements(By.TAG_NAME,"a")
        print("Links by Class : ", links)


        counter=1

        for link in links:
            print("===================================================")
            print(link)

            
            try:
                href = link.get_attribute("href")
                if "https://www.dice.com/job-detail/" in href:
                    print("HREF: ", href)
                    driver.execute_script("window.open('" + href + "', '_blank');")
                    print("In Loop: ", counter)

                    # Switch to the new tab
                    driver.switch_to.window(driver.window_handles[-1])

                    # Navigate to the href link
                    driver.get(href)

                    # Wait for the page to load
                    time.sleep(3)
                else:
                    continue
            except:
                print("Failed at href: ", href)
                continue
            
            

            try:
                # Click on "Easy Apply" and wait for the page to load
                easy_apply_button = driver.find_element(By.XPATH,"//*[@id='__next']/div/main/header/div/div/div[4]/div[2]/div[2]").click()
                # easy_apply_button.click()
                print("clicked on EASY APPLY BUTTON")
                time.sleep(5)

                # Click on "Next" and wait for the page to load
                next_button = driver.find_element(By.XPATH,"//*[@id='app']/div/span/div/main/div[4]/button[2]").click()
                # next_button.click()
                print("clicked on NEXT BUTTON")
                time.sleep(5)

                # Click on "Apply" and wait for the page to load
                apply_button = driver.find_element(By.XPATH,"//*[@id='app']/div/span/div/main/div[3]/button[2]").click()
                # apply_button.click()
                print("clicked on APPLY BUTTON")
                time.sleep(5)
                
                # # Check if the application was submitted successfully
                # success_message = driver.find_element(By.XPATH,'//div[contains(text(), "You have successfully applied")]')
                # if success_message:
                print("Successfully Submitted")

                # Close the tab
                driver.close()

                # Switch back to the main tab
                driver.switch_to.window(driver.window_handles[0])
                counter = counter +1 
                continue  # go to the next job if application was submitted successfully

            except:
                # Close the tab
                print("Already Applied or Not Easy Apply")
                driver.close()

                # Switch back to the main tab
                driver.switch_to.window(driver.window_handles[0])
                counter = counter +1 
                continue  # go to the next job if application was submitted successfully


            # except:
            #     print("Failed on Easy Apply Button")
            #     # driver.back()
            #     continue

        # Close the browser
        driver.quit()

# schedule the script to run every 6 hours
schedule.every(3).hours.do(apply_jobs_dice)

while True:
    schedule.run_pending()
    time.sleep(1)
