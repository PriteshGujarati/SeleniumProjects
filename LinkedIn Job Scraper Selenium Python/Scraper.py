from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os,random,sys,time
from  bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import pandas as pd

start_time = time.time()
jobs = []
def get_jobs(keyword, location, num_jobs, debugFlag):
    
    
    url ="https://www.linkedin.com/login"
    driver = webdriver.Chrome("chromedriver.exe")
    time.sleep(10)
    driver.implicitly_wait(10)
    driver.get(url)
    driver.maximize_window()
    time.sleep(10)
    driver.implicitly_wait(10)
    f = open('info.txt')
    lines = f.readlines()
    username = lines[0]
    password = lines[1]

    elementID = driver.find_element_by_id('username')
    elementID.send_keys(username)
    time.sleep(2)
    driver.implicitly_wait(2)
    elementID = driver.find_element_by_id('password')
    elementID.send_keys(password)
    driver.implicitly_wait(1)
    elementID.submit()

    time.sleep(7)
    driver.implicitly_wait(7)

    url =  "https://www.linkedin.com/jobs/search/?keywords="+keyword+"&location="+location
    driver.get(url)
    time.sleep(7)
    driver.implicitly_wait(7)

    #minimizing chat 
    driver.find_element_by_xpath('//*[@class="msg-overlay-bubble-header"]').click()
    #how many pages will need to get jobs 
    #rounds = int(num_jobs/25)     
    
    page_num = 2
    for i in range(0,4):
        #print("1")
        title = driver.title
        print("page num : ",page_num)
        try:
            get_job_details(driver,debugFlag)
        except NoSuchElementException:
            if(title != "data scientist Jobs in India | LinkedIn"):
                driver.back()
                time.sleep(5)
                driver.implicitly_wait(5)
                get_next_page(page_num,driver)
                print("page num except : ",page_num)
                time.sleep(5)
                driver.implicitly_wait(5)
        
        #print("3")
        driver.implicitly_wait(10)
        time.sleep(10)
        x ="https://www.linkedin.com/jobs/search/?currentJobId=1905091834&keywords=data%20scientist&location=India&start=75"
        title = driver.title
        get_next_page(page_num,driver)
        title = driver.title
        driver.implicitly_wait(10) 
        time.sleep(10)
        #print("4")
        page_num = page_num + 1    
        print("page num ++ : ",page_num)
        
    return "done"

def get_job_details(driver,debugFlag):

    #scrolling till buttom of page(online job section)
    target = driver.find_element_by_xpath('//div[@class="jobs-search-results jobs-search-results--is-two-pane"]')
    time.sleep(1)
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', target)
    driver.implicitly_wait(1)
    time.sleep(1)
    i = 24
    count = 0
    #print("5")
    while i > 0:
        #print("6")
        path = "//div[@class='job-card-container relative job-card-list job-card-container--clickable job-card-list--underline-title-on-hover  jobs-search-two-pane__job-card-container--viewport-tracking-"+str(i)+"']"
        
        try:
            #print("7")
            job = driver.find_element_by_xpath(path)
            job.click()
        except Exception as e:
            #print("8")
            #print(e)
            driver.implicitly_wait(5)
            time.sleep(5)
            title = driver.title
            if(title != "data scientist Jobs in India | LinkedIn"):
                #print("9")
                driver.back()
                time.sleep(5)
                driver.implicitly_wait(5)
                target = driver.find_element_by_xpath('//div[@class="jobs-search-results jobs-search-results--is-two-pane"]')
                driver.execute_script("return arguments[0].scrollIntoView(true);", target)
                time.sleep(5)
                driver.implicitly_wait(5)
                job = driver.find_element_by_xpath(path)
                job.click()
        
        
        collected_successfully = False
        #print("9")
        while not collected_successfully:
            t = True
            try:
                try:
         #           print("10")
                    title = driver.title
                    if(title != "data scientist Jobs in India | LinkedIn"):
          #              print("11")
                        driver.back()
                        driver.implicitly_wait(5)
                        time.sleep(5)
                        driver.implicitly_wait(5)
                        target = driver.find_element_by_xpath('//div[@class="jobs-search-results jobs-search-results--is-two-pane"]')
                        driver.execute_script("return arguments[0].scrollIntoView(true);", target)
                        time.sleep(5)
                        driver.implicitly_wait(5)
                        t = False
                        ##job = driver.find_element_by_xpath(path)
                        ##job.click()
           #         print("12")  
                    if(t== True):
                        company_name = driver.find_element_by_xpath('//a[@class= "jobs-details-top-card__company-url ember-view"]').get_attribute('text')
                    else:
                        t = True
                        company_name = "NA"
                except:
            #        print("13")
                    company_name = "NA"
             #   print("14")    
                location = driver.find_element_by_xpath('//span[@class= "jobs-details-top-card__bullet"]').text
                job_title = driver.find_element_by_xpath('//h2[@class= "jobs-details-top-card__job-title t-20 t-black t-normal"]').text
                collected_successfully = True
              #  print("15")
            except:
               # print("16")
                time.sleep(5)
        if debugFlag:
                print("Job Title: {}".format(job_title))
                print("Company Name: {}",company_name.strip())
                print("Location: {}".format(location))
       # print("17")
        count = count + 1
        i = i - 1
        jobs.append({"Job Title" : job_title,"Company Name" :company_name.strip(),"Location" : location,})
        #print("18")

def get_next_page(page_num,driver):
    try:
        #print("19")
        nextPage =  driver.find_element_by_xpath("//span[text() = '"+str(page_num)+"']")
        nextPage.click()
    except NoSuchElementException:
        #print("20")
        allpagesgroup =driver.find_elements_by_xpath("//li[@class = 'artdeco-pagination__indicator artdeco-pagination__indicator--number ember-view']")
        nextPage =  allpagesgroup[7]
        nextPage.click()    




get_jobs("data scientist","India",50 ,False)
df = pd.DataFrame(jobs)
df.to_csv("jobs.csv")
print(time.time()-start_time)