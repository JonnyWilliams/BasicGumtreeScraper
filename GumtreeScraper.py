#Author: Jon Williams
#This is a simple script design to scrape adds from GumTree and output them to a MS Excel spreadsheet .xlsx

#GumtreeScraper.py

# Import Librarys
import requests
import re
import csv
import xlwt
from bs4 import BeautifulSoup

# Define Variables
loc="cardiff" # e.g "Rhonnda+Cynon+taf", "Cardiff"
query="macbook"
category="for-sale" # For-Sale, All, Freebies etc

r=1 # excel row iterator

# Create Excel workbook and worksheet 
wbk = xlwt.Workbook()
sheet = wbk.add_sheet('sheet 1', cell_overwrite_ok=True)
                
# Write headers to excel worksheet
sheet.write(0,0,'Title')
sheet.write(0,1,'Price')
sheet.write(0,2,'Location')
sheet.write(0,3,'Date Listed')
sheet.write(0,4,'Description')
sheet.write(0,5,'Ad Number')
sheet.write(0,6,'URL of Ad')
                
# Start to scrape Gumtree
USER_AGENT = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"
REQUEST_HEADERS = {'User-agent': USER_AGENT,}

url1="http://www.gumtree.com/search?q=" +query +"&search_location=" +loc +"&category=" +category
while True:
    request = requests.get(url1, headers=REQUEST_HEADERS)
    if request.status_code == 200: # Got a valid response
        
        listing_results = []

        souped = BeautifulSoup(request.text, "html5lib") # Soupify page
                
        for listings_wrapper in souped.find_all("ul", class_="ad-listings"): # Find All listings on gumtree, each listing is enclosed in url tags with class ad-listings
            
            for listing in listings_wrapper.find_all("li", class_="offer-sale"): # Get details for each individual listing
                title = listing.find("a", class_="description").get("title")
                date = listing.find("div", class_="ad-features").find("span").get("title")
                if date is not None:
                    date = date[:10] # Only need first 10 characters for the date
                url = listing.find("a", class_="description").get("href")
                try:
                    price = listing.find("span", class_="price").string
                except:
                    price=0
                    pass
                summary = listing.find("div", class_="ad-description").find("span").string
                location =  listing.find("span", class_="location").string
                thumbnail = listing.find("img", class_="thumbnail").get("src")
                adref = listing.find("div", class_="ad-save").get("data-ad-id")
                
                # Write individual listing data to excelsheet
                sheet.write(r,0,title)
                sheet.write(r,1,price)
                sheet.write(r,2,location)
                sheet.write(r,3,date)
                sheet.write(r,4,summary)
                sheet.write(r,5,adref)
                sheet.write(r,6,url)
                r+=1
    else:
        # Some error handling
        print "Nothing found - Sever return code %s" % request.status_code
    
    # Find next button and set new URL1 for next page. If next button not found, then script completed.
    try:
        url1 = souped.find("li", class_=" pag-next").find("a").get("href")
    except:
        print "Finished scraping GumTree for " +query.upper() +" in " +loc.upper()
        print "The results can be found at /GumetreeOutput.xls"
        break

wbk.save('GumtreeOutput.xls')
