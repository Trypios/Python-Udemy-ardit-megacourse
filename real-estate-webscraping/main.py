# Parse a real-estate website and scrape data
# May not work as expected if the website has been updated since spring 2020

import requests, re, pandas
from bs4 import BeautifulSoup


# load webpage html source
request_headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
source_address = "http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/"
source = requests.get(source_address, headers=request_headers)
soup = BeautifulSoup(source.content, 'html.parser')

# Inspect homepage to extract numbers of subpages
pages = soup.find_all('div', {'class': 'propertyRow'})
subpages_count = soup.find_all("a", {"class":"Page"})[-1].text
print(subpages_count, "number of pages were found")

# Scrape classified listings
listings = []
base_url="http://web.archive.org/web/20160127020422/http://www.century21.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/"

for page_no in range(0, int(subpages_count)):
    url = f'{base_url}{page_no * 10}.html'
    source = requests.get(url)
    soup = BeautifulSoup(source.content, "html.parser")
    subpages = soup.find_all("div", {"class": "propertyRow"})

    # listing row: Address | Locality | Price | Beds | Area | Full Baths | Half Baths | Lot Size
    for page in subpages:
        temp_dict = {}

        temp_dict["Address"] = page.find_all("span", {"class", "propAddressCollapse"})[0].text
        try:
            temp_dict["Locality"] = page.find_all("span", {"class", "propAddressCollapse"})[1].text
        except Exception:
            temp_dict["Locality"] = None

        temp_dict["Price"] = page.find("h4", {"class", "propPrice"}).text.replace("\n", "").replace(" ", "")

        try:
            temp_dict["Beds"] = page.find("span", {"class", "infoBed"}).find("b").text
        except Exception:
            temp_dict["Beds"] = None
    
        try:
            temp_dict["Area"] = page.find("span", {"class", "infoSqFt"}).find("b").text
        except Exception:
            temp_dict["Area"] = None
    
        try:
            temp_dict["Full Baths"] = page.find("span", {"class", "infoValueFullBath"}).find("b").text
        except Exception:
            temp_dict["Full Baths"] = None

        try:
            temp_dict["Half Baths"] = page.find("span", {"class", "infoValueHalfBath"}).find("b").text
        except Exception:
            temp_dict["Half Baths"] = None

        for column_group in page.find_all("div", {"class": "columnGroup"}):
            for feature_group, feature_name in zip(column_group.find_all("span", {"class": "featureGroup"}),
                                                    column_group.find_all("span", {"class": "featureName"})):
                if "Lot Size" in feature_group.text:
                    temp_dict["Lot Size"] = feature_name.text

        listings.append(temp_dict)
        print(temp_dict)

# store data to csv
df = pandas.DataFrame(listings)
df.to_csv("listings.csv")
