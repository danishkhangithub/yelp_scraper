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
     
    current_page = 1 
     
    page = 10
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
        
       category = ''
     
       with open('category.json', 'r') as f:
         for line in f.read():
           category += line
       
       category = json.loads(category)
         
       states = ''
       
       with open('states.json', 'r') as f:
         for line in f.read():
           states += line
       
       states = json.loads(states)
       print(states)
       url = self.base_url + 'find_desc=%s' % category['category'] + '&find_loc=%s' % states['state']
       print(url)
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
            total_pages =  response.css('.text-align--center__09f24__1P1jK .css-e81eai::text').get()[5:7]
            
            
            next_page = response.css("a.next-link::attr(href)").get()
            
            #count +=1
            if next_page:
               
               yield response.follow(next_page, callback=self.parse_listing)
               self.current_page +=1  
               self.log('\n\n %s | %s\n\n ' %(self.current_page, total_pages))
               print('\n\n next_page:' ,next_page, '\n')
               
              
               
               
    def parse_cards(self,response):
          print('\n\nok\n\n')
         
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
            
          

          
# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(Yelp)
    process.start()
    
    #Yelp.parse_cards(Yelp, '')
    
    
