import bs4
import sqlite3
from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup
import re
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="code3.py")

for j in range(2, 32):

     my_url2 = 'https://rentalhomebd.com/searchrent/en/?page={}'.format(j)

     zclient2 = ureq(my_url2)

     data_html2 = zclient2.read()

     zclient2.close()

     data_soup2 = soup(data_html2, "html.parser")

     contents2 = data_soup2.findAll("div", {"class": "property-wraper"})

     for container in contents2:

         Title = container.findAll("div", {"class": "title"})
         Apm = Title[0].text.strip().replace("|\r\n", "")
         Ad_Title = Apm.replace("\xa0", "-")
         size = container.span.text.strip()
         amount = container.findAll(
             "span", {"class": "price pull-right text-right"})
         price_Title = amount[0].text
         D = re.split(', | /', price_Title)
         for j in range(len(D)):
            if(D[j] == 'month' or D[j] == ' month'):
                listing_category = 'RENT'
            else:
                listing_category = 'SALE'
         p1 = amount[0].text.split('BDT')
         p2 = p1[1].split()
         price = int(p2[0])
         property_location = container.address.text
         Adr = property_location.split(', ')
         Address = Adr[0]
         rooms = container.findAll("div", {"class": "attribute"})
         loom = rooms[0].text.strip()
         groom = loom.split()
         try:
            bed_rooms = groom[2]
            bath_rooms = groom[4]
         except:
             bath_rooms = "Only 1 Bathroom"

         wlink = "https://rentalhomebd.com"
         flink = container.img["src"]
         image = wlink + flink
         purl = container.findAll("div", {"class": "property-info"})
         url = purl[0]
         property_url = "https://rentalhomebd.com/" + url.a["href"]
         picture = None
         try:
             location = geolocator.geocode(Address)
             lat = location.latitude
             longi = location.longitude
         except:
            lat = None
            longi = None
         
         database = "db.sqlite3"
         conn = sqlite3.connect(database)

         conn.execute("""
         CREATE TABLE IF NOT EXISTS products_adverts (
            "id"	integer NOT NULL,
            "Ad_Title"	text NOT NULL,
            "price_Title"	text,
            "price"	integer NOT NULL,
            "property_location"	text NOT NULL,
            "Address" text NOT NULL,
            "listing_category"	varchar NOT NULL,
            "sq_ft"	text,
            "bed_rooms"	text NOT NULL,
            "bath_rooms"	text NOT NULL,
            "image"	text,
            "property_url" text,
            "picture" BLOB,
            "lat" real NOT NULL,
            "longi" real NOT NULL,
            PRIMARY KEY("id" AUTOINCREMENT)
         );""")

         cursor = conn.cursor()

         sqlite_insert_query = """INSERT INTO products_adverts
                         (Ad_Title, price_Title, price, property_location, Address, listing_category, sq_ft, bed_rooms, bath_rooms, image, property_url, picture, lat, longi) 
                          VALUES (?, ?, ?, ?, ?, ?, ? ,?, ?, ?, ?, ?, ?, ?);"""

         data_tuple = (Ad_Title, price_Title, price, property_location, Address, listing_category, size, bed_rooms, bath_rooms, image, property_url, picture, lat, longi)

         try:
             cursor.execute(sqlite_insert_query, data_tuple)
             conn.commit() 
             conn.close()
         except: 
            conn.close() 
