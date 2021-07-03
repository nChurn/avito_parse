import os
from seleniumwire import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

from selenium.webdriver.common.action_chains import ActionChains

from pprint import pprint

from bot import send_mess
from reader import read_phone_number

import asyncio

def interceptor(request):
     #print(request.headers)
     del request.headers['sec-fetch-mode']
     request.headers['sec-fetch-mode'] = 'cors'
     del request.headers['sec-fetch-site']
     request.headers['sec-fetch-site'] = 'same-origin'



class Parser():
    def __init__(self, driver):


        self.driver = driver
        self.post_title = None

    def goto(self):
        self.driver.get('https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&s=104')

    def check_new_posts(self):
        if self.post_title == None or self.driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[3]/div[3]/div[4]/div[1]/div[2]/div/div[2]/div[2]/a/h3').text != self.post_title:
            self.post_title = self.driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[3]/div[3]/div[4]/div[1]/div[2]/div/div[2]/div[2]/a/h3').text
            return True
        return False

#    def open_last_page(self):
#        href = self.driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[3]/div[3]/div[4]/div[1]/div[2]/div/div[2]/div[2]/a').get_attrebute('href')
#        self.driver.get(href)

    def open_last_page(self):
        self.driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[3]/div[3]/div[4]/div[1]/div[2]/div/div[2]/div[3]').click()
        #pprint(self.driver.)

    async def parse_and_send(self):
        self.driver.switch_to_window(self.driver.window_handles[1])
        #self.div = self.driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[3]/div[3]/div[4]/div[1]/div[5]/div/div[2]/div[4]/div/div')
        #pprint(self.div)
        #time.sleep(1000)
        
        #pprint(self.driver.page_source)
        #/html/body/div[3]/div[1]/div[3]/div[5]/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div/span
#        try:
#            info = self.driver.find_element_by_class_name('seller-info/label').text
#            print(info)
#        except:
#            print('ne rabotait')
#            self.driver.close()
#            self.driver.switch_to_window(self.driver.window_handles[0])

        try:
                try:
                    # Если агенство - этих полей нет
                    self.owner = self.driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[3]/div[4]/div[2]/div[1]/div/div[3]/div/div/div[1]/div[1]/div/a').text
                    self.owner_href = self.driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[3]/div[4]/div[2]/div[1]/div/div[3]/div/div/div[1]/div[1]/div/a').get_attribute('href')
                except:
                    
                    
                    self.driver.close()
                    self.driver.switch_to_window(self.driver.window_handles[0])
                    print('Agenstvo')
                    return
                
                #time.sleep(10000)
                
                #with open('page.html', 'w') as file:
                #    file.write(self.driver.page_source)
                buttons = self.driver.find_elements_by_xpath('//*[contains(text(), "Показать телефон")]')
                for button in buttons:
                    try:(button.click())
                    except: pass
                    
            # button[1].click()
                #self.driver.implicitly_wait(10)
                #ActionChains(self.driver).move_to_element(button).click(button).perform()
                
                #time.sleep(10)
                #self.driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[3]/div[4]/div[2]/div[1]/div/div[2]/div/div/div/div[1]/span/span/div/div/button").click()


                time.sleep(3)
                phone_base = self.driver.find_element_by_xpath('/html/body/div[10]/div/div/div/div/div[1]/img').get_attribute('src')
                self.phone = read_phone_number(phone_base)
            
                
                try:

                    self.coast = self.driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[3]/div[5]/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div/span').text
                except:
                    self.coast = self.driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[3]/div[4]/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div/span').text
                print(self.coast)
                
                self.post_url = self.driver.current_url

                #self.address = self.driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[3]/div[4]/div[1]/div[2]/div[4]/div/div[1]/div[1]/div/span').text
                self.metros = self.driver.find_elements_by_class_name('item-address-georeferences-item')

                
                #time.sleep(100)
                #print(self.phone)
                print(self.metros)
                print(self.owner)
                print(self.owner_href)
                await send_mess(self)
                self.driver.close()
                self.driver.switch_to_window(self.driver.window_handles[0])
                return
            
        except:
            pass

    async def parse_last_post_if_exists(self):
        #self.driver.refresh()
        if self.check_new_posts():
            
            self.open_last_page()
            await self.parse_and_send()
        else:
            pass            


async def main():
    #options = {
     #   'httpProxy': '103.137.91.250:8080',
      #  'httpsProxy': '36.89.126.183:8080',
        #'no_proxy': 'localhost,127.0.0.1,dev_server:8080',
        #'custom_authorization': 'Bearer mytoken123'  # Custom Proxy-Authorization header value
    
    #}
    options = {
    'suppress_connection_errors': False,  # Show full tracebacks for any connection errors
    #"headless":  True,
    }
    opt = Options()
    opt.add_argument('--headless')

    driver_path = '/usr/bin/chromedriver'
    #driver_path = '/usr/local/bin/geckodriver
    driver = webdriver.Chrome(driver_path, seleniumwire_options=options, chrome_options=opt)
    #driver = webdriver.Chrome(driver_path)
    driver.request_interceptor = interceptor
    parser = Parser(driver) 
    parser.goto()
    
    #parser.open_last_page()
    while True:
        await parser.parse_last_post_if_exists()
        time.sleep(60)
        parser.driver.refresh()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())