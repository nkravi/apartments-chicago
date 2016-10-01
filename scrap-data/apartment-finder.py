
# coding: utf-8

# ## This code scraches the http://www.apartmentfinder.com/

# In[1]:

# imports 
from bs4 import BeautifulSoup
import urllib


# In[7]:

def read_page(url):
    r = urllib.urlopen(url).read()
    return BeautifulSoup(r,'html.parser')


# In[14]:

#read pages
base_url = "http://www.apartmentfinder.com/Illinois/Chicago-Apartments/Page"
page_lst = [read_page(base_url+str(pageNum)) for pageNum in range(1,31)]


# In[15]:

#len(page_lst)


# In[51]:

# get location
def get_location(soup):
    return [s.span.text for s in soup.findAll("div", { "class" : "location ellipses row" })] + [s.div.span.text for s in soup.findAll("div", { "class" : "location row" })]


# In[62]:

# get rent
def get_rent(soup):
    return [s.text for s in soup.findAll("span", { "class" : "altRentDisplay" })]


# In[71]:

# get unit lable
def get_unit_label(soup):
    return [s.text for s in soup.findAll("span", { "class" : "unitLabel" })]


# In[65]:

def collect_dat(fun):
    lst = []
    for soup in page_lst:
        lst += fun(soup)
    return lst


# In[68]:

location_lst = collect_dat(get_location)


# In[ ]:

rent_lst = collect_dat(get_rent)


# In[73]:

unit_label_lst = collect_dat(get_unit_label)


# In[84]:

#len(location_lst) == len(rent_lst) == len(unit_label_lst) == 750


# In[97]:

def process_rent(rent):
    tmp = rent.strip().replace('$','').replace(',','').split('-')
    if len(tmp) == 2:
        return (tmp[0].strip(),tmp[1].strip())
    elif len(tmp) == 1:
        return (tmp[0].strip(),tmp[0].strip())
    else:
        return (0,0)


# In[101]:

def process_unit_label(unitLabel):
    tmp = unitLabel.strip().replace('Beds','').replace('Bed','').split('-')
    if len(tmp) == 2:
        return (tmp[0].strip(),tmp[1].strip())
    elif len(tmp) == 1:
        return (tmp[0].strip(),tmp[0].strip())
    else:
        return (0,0)


# In[98]:

processed_rent_lst = map(process_rent,rent_lst)


# In[102]:

processed_unit_label = map(process_unit_label,unit_label_lst)


# In[114]:

processed_location_lst = map(lambda x : (x.split()[-1].strip(),x), location_lst)


# In[116]:

#len(processed_rent_lst) == len(processed_unit_label) == len(processed_location_lst) == 750


# In[124]:

def covert_to_string(res):
    address,rent,beds = res
    zipcode,addr = address
    min_rent,max_rent = rent
    min_bed,max_bed = beds
    return format('%s|%s|%s|%s|%s|%s')%(zipcode,addr,min_rent,max_rent,min_bed,max_bed)


# In[118]:

result = zip(processed_location_lst, processed_rent_lst,processed_unit_label)


# In[125]:

result_str = map(covert_to_string,result)


# In[126]:

#len(result_str) == 750


# In[127]:

print 'zipCode|Address|minRent|maxRent|minBed|maxBed'


# In[ ]:

for r in result_str:
    print r

