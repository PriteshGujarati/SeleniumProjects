from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd

keyword = "data-scientist"
location = "India"

def get_jobs(keyword, location, num_jobs,debug):
    
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome("chromedriver.exe", options=options)
    driver.maximize_window()
    url = "https://www.glassdoor.co.in/Job/"+location+"-"+keyword+"-jobs-SRCH_IL.0,5_IN115_KO6,20.htm"
    driver.get(url)
    jobs = [] 
    while len(jobs) < num_jobs:
        time.sleep(10)
        #check if sign up box is there or not, if yes remove it by clicking on X
        try:
            driver.find_element_by_class_name("selected").click()
        except ElementClickInterceptedException:
            pass
        time.sleep(5)
        try:
            driver.find_element_by_xpath("//*[@class='SVGInline-svg modal_closeIcon-svg']").click()
        except:
            pass

        #Going through each job in this page
        job_buttons = driver.find_elements_by_class_name("jl") 
        for job_button in job_buttons:  
            job_button.click()   
            time.sleep(1)
            collected_successfully = False
            
            while not collected_successfully:
                try:
                    company_name = driver.find_element_by_xpath('.//div[@class="employerName"]').text
                    location = driver.find_element_by_xpath('.//div[@class="location"]').text
                    job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
                    job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(5)
           
            try:
                rating = driver.find_element_by_xpath('.//span[@class="rating"]').text
            except NoSuchElementException:
                rating = -1 #You need to set a "not found value. It's important."

            #Printing for debugging
            if(debug == True):
                print("Job Title: {}".format(job_title))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))
                
            try:
                driver.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="overview"]').click()
                time.sleep(1)
                try:
                    
                    headquarters = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                except NoSuchElementException:
                    headquarters = -1

                try:
                    size = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1

            except NoSuchElementException:  
                headquarters = -1
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
          
            if(debug == True):
                print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("###################################################")
            
            #adding to jobs
            jobs.append({"Job Title" : job_title,"Job Description" : job_description,
            "Rating" : rating,"Company Name" : company_name,"Location" : location,"Headquarters" : headquarters,"Size" : size,
            "Founded" : founded,"Type of ownership" : type_of_ownership,"Industry" : industry,"Sector" : sector,
            "Revenue" : revenue})
        #for next page 
        try:
            driver.find_element_by_xpath('.//li[@class="next"]//a').click()
        except NoSuchElementException:
            break

    return pd.DataFrame(jobs)

df = get_jobs(keyword, location, 50, True)
df.to_csv("GDjobs.csv")
