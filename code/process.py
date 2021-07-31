from bs4 import BeautifulSoup
import json
import re
import boto3

s3 = boto3.client('s3')

UNPROCESSED_BUCKET = 'unprocessed-bucket-tvw'
PROCESSED_BUCKET = 'processed-bucket-tvw'

output = {}

def read_content(filename, bucket=None):
    if bucket is None:
        with open(filename, 'rb') as f:
            return f.read()
    
    else:
        return s3.get_object(Bucket=bucket, Key=filename)['Body'].read()

for object in s3.list_objects(Bucket=UNPROCESSED_BUCKET, Prefix='job_page')['Contents']:
    filename = object['Key']
    content = read_content(filename, UNPROCESSED_BUCKET)

    soup = BeautifulSoup(content, 'html5lib')

    id_num = filename.split('/')[-1].split('.')[0]

    job_title = soup.select_one('#titletextonly').contents
    job_title = ''.join(job_title)

    job_description = soup.select_one('#postingbody').contents
    job_description = ''.join(re.sub('^<br/>', '\n', str(line)) for line in job_description[2:])

    output[id_num] = {'title': job_title, 'description': job_description}

s3.put_object(Body=json.dumps(output), Bucket=PROCESSED_BUCKET, Key='processed.json')