from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

DRIVER_PATH = r"C:\Users\hp\Desktop\chromedriver.exe"
QUERY_URL = 'https://eraindia.org/members-directory/'

driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.maximize_window()
driver.get(QUERY_URL)

try:
    data = []
    while True:
        time.sleep(5)
        listings = driver.find_elements_by_xpath('//*[@id="wpbdp-listings-list"]/div[contains(@class,"wpbdp-listing")]')
        for elem in listings:
            elem_id = elem.get_attribute('id')
            title = driver.find_element_by_xpath(f'//div[@id="{elem_id}"]//div[@class="listing-title"]').text
            try:
                site = driver.find_element_by_xpath(f'//div[@id="{elem_id}"]//*[contains(@class,"wpbdp-field-website")]//div[@class="value"]').text
            except:
                site = 'NA'
            try:
                mail = driver.find_element_by_xpath(f'//div[@id="{elem_id}"]//*[contains(@class,"wpbdp-field-email")]//div[@class="value"]').text
            except:
                mail = 'NA'
            try:
                address = driver.find_element_by_xpath(f'//div[@id="{elem_id}"]//div[starts-with(@class, "address-info")]/div').text
            except:
                address = 'NA'
                
            # print(title)
            data.append([title, site, mail, address])
                
        try:
            next_btn = driver.find_element_by_xpath('//span[@class="next"]/a')
            next_btn.location_once_scrolled_into_view
            next_btn.click()
        except NoSuchElementException:
            break
        
except Exception as e:
    print('First Exception -->', e)

finally:
    driver.quit()
    
try:
    my_df = pd.DataFrame(data)
    headerList=['Company','Website','Email','Address']
    file_name = f'ERA_data.csv'
    my_df.to_csv(file_name, index=False, header=headerList)
except Exception as e:
    print(f'Error in Pandas --> {e}')
    