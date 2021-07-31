import boto3
import requests
from bs4 import BeautifulSoup
import random
import time
import logging

#print(soup.prettify())

s3 = boto3.client('s3')

UNPROCESSED_BUCKET = 'unprocessed-bucket-tvw'
PROCESSED_BUCKET = 'processed-bucket-tvw'

# s3.put_object(Body=soup.prettify(), 
#               Bucket='unprocessed-bucket-tvw', 
#               Key='test.html')
logging.basicConfig(filename='logs/collect.log', 
                    encoding='utf-8', 
                    level=logging.DEBUG)

def write_content(content, filename, bucket=None):
    if bucket is None:
        with open(filename, 'wb') as f:
            f.write(content)
    else:
        s3.put_object(Body=content, Bucket=bucket, Key=filename)

def get_main_page():
    URL = "https://chicago.craigslist.org/d/software-qa-dba-etc/search/sof"

    r = requests.get(URL)

    write_content(r.content, f'search_results/{int(time.time())}.html', bucket=UNPROCESSED_BUCKET)
    with open(f'test_data/search_results/{int(time.time())}.html', 'wb') as f:
        f.write(r.content)
    
    logging.info('Got main page')
    
    return BeautifulSoup(r.content, 'html5lib')

def random_sleep(min=0.5, max=1.5):
    x = random.random()
    sleep_time = x * (max - min) + min
    time.sleep(sleep_time)

def get_sub_pages(soup):
    for link in soup.select('.result-title, .hdrlnk'):
        url = link['href']
        id_file = url.split('/')[-1]

        r = requests.get(link['href'])

        write_content(r.content, f'job_page/{id_file}', bucket=UNPROCESSED_BUCKET)
        
        logging.info(f'Got and saved {url}')

        random_sleep()

soup = get_main_page()
get_sub_pages(soup)
