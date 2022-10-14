import scrapy
import pandas as pd
df = pd.read_csv('F:\Web Scraping\Golabal\keywords.csv')
base_url = 'https://www.yellowpages.com/search?search_terms=restuarant&geo_location_terms={}&page=1'

class YellowSpider(scrapy.Spider):
    name = 'yellow'
    def start_requests(self):
        for index in df:
            yield scrapy.Request(base_url.format(index), cb_kwargs={'index':index})

    def parse(self, response, index):
        showing = response.css("div.pagination span::text").get()
        pages1 = showing.split('of ')
        pages2 = int(pages1[1])        
        total_pages = int(pages2/30)      
        current_page =response.css("span.disabled::text").get()  
        url = response.url        
        if total_pages and current_page:
            if int(current_page) ==1:
                for i in range(2, int(total_pages)+1): 
                    min = 'page='+str(i-1)
                    max = 'page='+str(i)
                    url = url.replace(min,max)  
                    # print(url)                          
                    yield response.follow(url, cb_kwargs={'index':index})       

        links = response.css("a.business-name::attr(href)")
        for link in links:           
            yield response.follow("https://www.yellowpages.com"+link.get(),  callback=self.parse_item, cb_kwargs={'index':index})  
           
    def parse_item(self, response, index): 
        print(".................")        
        website = response.css("a.website-link::attr(href)").get()
        print(website)        
        name = response.css("h1.business-name::text").get()
        print(name)     
        location = response.xpath("//section[@id='details-card']//p[2]/text()").get()
        print(location)
        phone = response.css("a.phone strong::text").get()
        print(phone)
        categories = response.xpath("//dd[@class='categories']/div/a/text()").getall()
        print(categories)
      

        yield{   
            'name' : name,  
            'phone' : phone,
            'categories' : categories,
            'location' : location,  
            'state_name' : index,
            'website' : website,
            'yellowpages_url' : response.url,              
                
        }
