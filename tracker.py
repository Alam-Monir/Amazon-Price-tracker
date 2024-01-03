import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from datetime import datetime
from amazon_config import(
    Name,
    currency,
    filters,
    base_url,
    get_web_driver_options,
    set_ignore_certificate_error,
    set_browser_as_incognito,
    set_ignore_ssl_errors,
    get_chrome_web_driver,
    set_automation_as_head_less
)

class generate_report:
    def __init__(self, file_name, filters, base_link, currency, data):
        self.data = data
        self.file_name = file_name
        self.filters = filters
        self.base_link = base_link
        self.currency = currency
        # report = {
        #     'title': self.file_name,
        #     'date': self.get_now(),
        #     #'best_item': self.get_best_item(),
        #     'currency': self.currency,
        #     'filters': self.filters,
        #     'base_link': self.base_link,
        #     'products': self.data
        # }
        print("Creating report...")
        dataframe = pd.DataFrame(data, index=None)
        dataframe.to_csv(r"E:\Github\Amazon-Price-tracker\sample_dataset0.csv")
        print("Done...🚀")

    def get_now(self):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        return dt_string


class amazon_api:
    def __init__(self,search,filters,base_url,currency):
        self.search=search
        self.base_url=base_url
        options = get_web_driver_options()
        #set_automation_as_head_less(options)
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        set_ignore_ssl_errors(options)
        self.driver = get_chrome_web_driver(options)
        self.currency = currency
        self.price_filter = f"&rh=p_36%3A{filters['min']}00-{filters['max']}00"
        
        pass
    
    def get_product_links(self):
        self.driver.get(self.base_url)
        element = self.driver.find_element(By.ID,"twotabsearchtextbox")
        element.send_keys(self.search)
        element.send_keys(Keys.ENTER)
        time.sleep(2)
        self.driver.get(f'{self.driver.current_url}{self.price_filter}')
        print(f"Our url: {self.driver.current_url}")
        time.sleep(2)
        result_list = self.driver.find_elements(By.CLASS_NAME, 's-result-list')
        links = []
        for i in range(1):
            self.driver.get(f'{self.driver.current_url}{self.price_filter}&page={i+1}')
            time.sleep(3)
            result_list = self.driver.find_elements(By.CLASS_NAME, 's-result-list')

            try:
                results = result_list[0].find_elements(By.XPATH, "//div[@data-cy='title-recipe']/h2/a")
                for link in results:
                    href = link.get_attribute('href')
                    links.append(href)
                    #links= [link.get_attribute('href') for link in results]
                    #return links
            except Exception as e:
                print('Did not get any products')
                print(e)
                #return links
        return links
    
    def get_asins(self,links):
        return [self.get_asin(link) for link in links]
    
    def get_asin(self,links):
        if links[21:26]=='/sspa' :
             return links[(links.find('p%2F') + 4):(links.find('%2Fref'))]
            
        else:
            return links[links.find('/dp/') + 4:links.find('/ref')]
    
    def short_url(self,asin):
        return self.base_url + 'dp/' + asin
    
    def product_info(self,links):
        asins=self.get_asins(links)
        products=[]
        for asin in asins:
            product = self.get_single_product_info(asin)
            if product:
                products.append(product)
        return products
    
    def get_single_product_info(self,asin):
        product_short_url = self.short_url(asin)
        print(f"Product ID: {asin} - getting data from {product_short_url}")
        self.driver.get(f'{product_short_url}')
        time.sleep(2)
        title = self.get_title()
        seller = self.get_seller()
        price = self.get_price()
        stars = self.get_stars()
        ratings = self.get_ratings()
        if title and seller and price:
            product_info = {
                'asin': asin,
                'url': product_short_url,
                'title': title,
                'seller': seller,
                'price in RS': price,
                'stars': stars,
                'ratings':ratings
            }
            return product_info
        return None
    
    def get_title(self):
        try:
            return self.driver.find_element(By.XPATH, "//div[@id ='titleSection']/h1/span").text
        except Exception as e:
            print(e)
            print(f"can't find title {self.driver.current_url}")

    def get_seller(self):
        try:
            return self.driver.find_element(By.XPATH,"//div[@class ='a-section a-spacing-mini']/div/a[1]/span[1]").text
        except Exception as e:
            print(e)
            print(f"can't find seller {self.driver.current_url}")

    def get_price(self):
        price=None
        try:
            price=self.driver.find_element(By.XPATH,"//div[@class='a-section a-spacing-none aok-align-center']/span[2]/span[2]/span[2]").text
            price = self.convert_price(price)
            return price
        except NoSuchElementException:
           try:
               availability = self.driver.find_element(By.XPATH,"//div[@class='a-button-stack']/span/span/span/a").text
               if ' See All Buying Options ' in availability:
                   price = self.driver.find_element(By.XPATH,"//span[@id='aod-price-1']/div/span[2]/span[2]/span[2]").text
                   price = self.convert_price(price)
           except Exception as e:
               print(e)
               print(f"Can't get price of a product - {self.driver.current_url}")
               return None
        except Exception as e:
            print(e)
            print(f"Can't get price of a product - {self.driver.current_url}")
            return None
        return price
    
    def convert_price(self,price):
        int_price= price.replace(",","")
        return int_price
    
    def get_stars(self):
        try:
            return self.driver.find_element(By.XPATH, "//div[@id='averageCustomerReviews_feature_div']/div/span/span/span/a/span").text
        except Exception as e:
            print(e)
            print(f"can't find stars {self.driver.current_url}")
    
    def get_ratings(self):
        try:
            return self.driver.find_element(By.XPATH, "//div[@id='averageCustomerReviews']/span[3]/a/span").text
        except Exception as e:
            print(e)
            print(f"can't find ratings {self.driver.current_url}")



    def run(self):
        print('Starting scripts..')
        print(f"Looking for {self.search} products.")
        links=self.get_product_links()
        #print(len(links))
        if not links:
            print("Stopped script.")
            return
        print(f"Got {len(links)} links to products...")
        print("Getting info about products...")
        products = self.product_info(links)
        print(f"Got info about {len(products)} products...")
        self.driver.quit()
        return products
    

    

if __name__ == '__main__':
        amazon = amazon_api(Name, filters, base_url, currency)
        data = amazon.run()
        generate_report(Name, filters, base_url, currency, data)
