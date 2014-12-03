from amazon_scraper import AmazonScraper
import warnings
from bs4 import BeautifulSoup
import time

#Global variables and settings
warnings.filterwarnings("ignore")
AWS_ACCESS_KEY_ID = "AKIAIETM24OXNYX6EKAQ"
AWS_SECRET_ACCESS_KEY = "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"
AWS_ASSOCIATE_TAG = "personaltwi08-20"



#This function takes in a product object and returns the # of 1-5 star ratings as a list
def ratings(product):
    ratings = [0, 0, 0, 0, 0]
    reviews_div = product.soup.find('div', class_='reviews')
    if reviews_div:
        for rating, rating_class in [
            (4, 'histoRowfive'),
            (3, 'histoRowfour'),
            (2, 'histoRowthree'),
            (1, 'histoRowtwo'),
            (0, 'histoRowone'),
        ]:
            rating_div = reviews_div.find('div', class_=rating_class)
            if rating_div:
                # no ratings means this won't exist
                tag = rating_div.find('div', class_='histoCount')
                if tag:
                    value = tag.string
                    value = value.replace(',', '')
                    ratings[rating] = int(value)
        return ratings

    table = product.soup.find('table', id='histogramTable')
    if table:
        for rating, row in zip([4,3,2,1,0], table.find_all('tr', class_='a-histogram-row')):
            # get the third td tag
            children = [child for child in row.find_all('td', recursive=False)]
            td = children[2]
            data = td.find('a')
            if data:
                # number could have , in it which fails during int conversion
                value = data.string
                value = value.replace(',', '')
                ratings[rating] = int(value)
        return ratings

    return ratings


#Main function of this program

def main():
    #Create Scraper
    a = AmazonScraper(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_ASSOCIATE_TAG)
    
    #Get list of items from excel file
    
    
    #Look up required item
    p = a.lookup(ItemId='B0014IKQKG')
    
    
    for i in range(0,3):
        rs = a.reviews(URL=p.reviews_url)
        if(len(rs.ids) == 0):
            time.sleep(3)
        else:
            break
    r = a.review(Id=rs.ids[0])
    
    print r.text
    
    #print(ratings(p))

main()
