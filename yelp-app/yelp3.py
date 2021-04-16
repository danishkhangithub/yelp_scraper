# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import os
import json
import datetime
import csv
import PySimpleGUI as sg





# property scraper class
class Yelp(scrapy.Spider):
    # scraper name
    name = 'home bussiness'
    base_url = 'https://www.yelp.com/search?'
    params = {
     'find_desc': 'Home Cleaning',
     'find_loc':'North Dallas, Dallas, TX',
     #'start' : ''
     }
     
    current_page = 1 
     
    page = 0
    # headers
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
        
     }
    #params['start'] = page
    try:
       os.remove('abx.csv')
    except OSError:
       pass   
    # custom settings
    custom_settings = {
        'CONCURRENT_REQUEST_PER_DOMAIN': 2,
        'DOWNLOAD_DELAY': 3
    }

    # general crawler
    def start_requests(self):
            url = self.base_url + urllib.parse.urlencode(self.params)
            # initial HTTP request
            yield scrapy.Request(
                url=url,
                headers=self.headers,
               
                callback=self.parse_listing
            )
            
    def parse_listing(self, response):
            
            lists = response.css('h4[class="css-1l5lt1i"]')
            
            for link in lists:
                link = link.css('a::attr(href)').get() 
                link =  'https://www.yelp.com/' + link            
                #print('\n\nlink:',link,'\n\n')
                #yield response.follow(link, headers = self.headers, callback = self.parse_cards)
                break
            #total_pages =  response.css('.text-align--center__09f24__1P1jK .css-e81eai::text').get()[5:7]
            total_pages = 5
            
            #self.page +=10 
            for i in range(0,total_pages):
                #self.page +=10   
                if (int(self.page/10) < int(total_pages)):
                    self.page +=10 
                    self.log('\n\n %s | %s\n\n ' %(self.page/10, total_pages))
                    next_page = response.url + '&start=' + str(self.page)
                    print('\n\nnext_page:', next_page)
                    yield scrapy.Request(url = next_page, headers = self.headers, callback = self.parse_listing) 
            
    def parse_cards(self,response):
    
#         '''
#         content = ''
#         with open('Yelp1.html', 'r' ) as f:
#           for line in f.read():
#             content += line
#         response = Selector(text=content) 
#         '''
#         features = {
#          'name' : response.css('h1[class="css-11q1g5y"]::text').get(),
#          'url' : response.url,
#          'Phone number' : response.css('.css-aml4xx+ .css-1h1j0y3::text').get(),
#          'Contractor' : response.css('.margin-r1__373c0__zyKmV .css-166la90::text').get()
# 
#          
#         
#         }
#         print(features)
            
          
         
         '''
         with open('res.csv', 'a') as f:
           writer = csv.DictWriter(f, fieldnames = features.keys())
           writer.writerow(features)
         '''
          
# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(Yelp)
    process.start()
    
    #Yelp.parse_cards(Yelp, '')
    
    
