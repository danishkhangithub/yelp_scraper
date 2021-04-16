# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import os
import json
import datetime
import csv

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
    page = 0
    current_page = 1
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
        'DOWNLOAD_DELAY': 1
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
                
            try:    
                
              #self.params['start'] = self.page
              try:
                  total_pages =  response.css('.text-align--center__09f24__1P1jK .css-e81eai::text').get()[5:7]
                  print('\ntotal pages:',total_pages)

 
                  self.page +=10
                  self.current_page +=1
                  

              except Exception as e:
                 total_pages = 1
                 print('totl:',total_pages)
                 print('PAGE %s | %s ' % (self.current_page, total_pages)) 
                 
 
 
              if int(self.page/10) <= int(total_pages):
                self.log('\n\n %s | %s\n\n ' %(self.page/10, total_pages))
                next_page = response.url + '&start=' + str(self.page)
                yield response.follow(url = next_page, headers = self.headers, callback = self.parse_listing) 
            except:
             print('only single page',self.current_page)

           
    def parse_cards(self,response):
      print('\nok\n')   
      
# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(Yelp)
    process.start()
    
    #Yelp.parse_cards(Yelp, '')
    
    
