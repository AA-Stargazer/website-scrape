import pandas as pd
import requests
import random
from scrapy.selector import Selector
from traceback import print_exc
import time





if __name__ == "__main__":
    
    
    user_agents = [
            'https://www.omvic.on.ca/RegistrantSearchM/SearchResult/Dealer.aspx?DealerName=zz&City=null&PostalCode=null&URL=null', 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36', 
            'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0', 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 YaBrowser/22.9.5.710 Yowser/2.5 Safari/537.36', 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.77'
    ]

    url_base = 'https://www.sourcewell-mn.gov/contract-search'

    next_button = '?keyword=&category=All'
    
    main_list = []

    while next_button:

        try:
            response = requests.get(
                url_base + next_button
                # , proxies = {
                #     "http": "",
                #     "https": ""
                # }
                , headers = {
                    'user-agent': random.choice(user_agents),   
                    'Accept-Encoding': 'gzip, deflate',     
                    'Accept': '*/*', 
                    'Connection': 'keep-alive'  
                }
                , stream = True
            )
        except ConnectionError:
            
            print_exc()
            
            time.sleep(5)
            
            response = requests.get(
                url_base + next_button
                # , proxies = {
                #     "http": "",
                #     "https": ""
                # }
                , headers = {
                    'user-agent': random.choice(user_agents),   
                    'Accept-Encoding': 'gzip, deflate',     
                    'Accept': '*/*', 
                    'Connection': 'keep-alive'  
                }
                , stream = True
            )

        if int(response.status_code) != 200:
        
            raise
        selector = Selector(text=response.content)
        
        cards = selector.xpath('//div[contains(@class, "row")]/div[contains(@class, "row")]')
        for card in cards:
            
            tmp_dict = {}
            
            suppliers = card.xpath('.//h3/a')
            
            suppliers_text = suppliers.xpath('./text()').get().replace('\n', '')
            
            # suppliers_url = suppliers.xpath('./@href').get()

            tmp_dict['Suppliers'] = suppliers_text

            # tmp_dict['Suppliers URL'] = suppliers_url
            
            
            title = card.xpath('.//h3/following-sibling::p[contains(@class, "description")]/text()').get().replace('\n', '')

            tmp_dict['Title'] = title

            numbers = card.xpath('.//h3/following-sibling::p[contains(@class, "number")]/text()').get().replace('\n', '')

            numbers = numbers.split(' | ')

            tmp_dict['Contact Number'] = numbers[0].replace('\n', '')

            tmp_dict['Expiration'] = numbers[1].split('Maturity Date:')[-1].replace('\n', '')

            main_list.append(tmp_dict)
        next_button = selector.xpath('//ul[contains(@class, "full")]//a[contains(@href, "&page=") and //*[contains(., "page")] ]//span[@aria-hidden]/parent::a[1][contains(@title, "next")]/@href').get()

        print(next_button)        
    pd.DataFrame(main_list).to_csv('output.csv', index=False)