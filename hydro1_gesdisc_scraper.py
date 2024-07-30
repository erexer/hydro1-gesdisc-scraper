import regex as re
import requests
from bs4 import BeautifulSoup
import os


DATA_DIR = "nldas2_data"


def get_year_links(url):

    # create response object  
    try:
        r = requests.get(url)
    except Exception as e:
        print(e)

    # create beautiful-soup object  
    soup = BeautifulSoup(r.text,'html.parser')  
      
    # find all links on web-page  
    links = soup.findAll('a')  
  
    # filter the links ending with a year  
    year_links = [url + link['href'] for link in links if re.search("[0-9][0-9][0-9][0-9]/$", link['href'])]
    year_links = remove_duplicates(year_links)

    return year_links  


def get_day_links(url):
    # create response object  
    try:
        r = requests.get(url)
    except Exception as e:
        print(e)

    # create beautiful-soup object  
    soup = BeautifulSoup(r.text,'html.parser')  
      
    # find all links on web-page  
    links = soup.findAll('a')  

    # filter the links ending with a year  
    day_links = [url + link['href'] for link in links if re.search("[0-3][0-9][0-9]/$", link['href']) and not link['href'].endswith("NLDAS_FORA0125_H.002/")]
    day_links = remove_duplicates(day_links)

    return day_links  


def remove_duplicates(a):
    # Not order preserving
    return list(set(a))
    

def get_grb_xml_links(url):  
      
    # create response object  
    try:
        r = requests.get(url)
    except Exception as e:
        print(e)
      
    # create beautiful-soup object  
    soup = BeautifulSoup(r.text,'html.parser')  
      
    # find all links on web-page  
    links = soup.findAll('a')  
  
    # filter the links ending with .grb and .xml  
    grb_xml_links = [url + link['href'] for link in links if link['href'].endswith('grb') or link['href'].endswith('xml')]  
    grb_xml_links = remove_duplicates(grb_xml_links)
  
    return grb_xml_links  

def download_file(grb_xml_links, year, day):  
  
    for link in grb_xml_links:  
  
        '''iterate through all links in grb_xml_links  
        and download them one by one'''
          
        # obtain filename by splitting url and getting  
        # last string 
        file_name = f"{DATA_DIR}/{year}/{day}/{link.split('/')[-1]}"
  
        # create response object  
        r = requests.get(link, stream = True)  
          
        # # download started  
        with open(file_name, 'wb') as f:  
            for chunk in r.iter_content(chunk_size = 1024*1024):  
                if chunk:  
                    f.write(chunk)  
          
    print (f"{year}/{day} files downloaded!") 
    return

if __name__ == "__main__":  

    url = "https://hydro1.gesdisc.eosdis.nasa.gov/data/NLDAS/NLDAS_FORA0125_H.002/"

    for year_link in get_year_links(url):

        year = year_link.split('/')[-2]

        for day_link in get_day_links(year_link):

            day = day_link.split('/')[-2]

            # make directory if it doesn't exist
            path = os.path.join(os.getcwd(), DATA_DIR, year, day) 
            os.makedirs(path, exist_ok=True) 

            grb_xml_links = get_grb_xml_links(day_link)
            download_file(grb_xml_links, year, day)

