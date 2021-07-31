from bs4 import BeautifulSoup
import json
import re
import boto3

def lambda_handler(event, context):
    output = {}
    s3 = boto3.client('s3')

    UNPROCESSED_BUCKET = 'unprocessed-bucket-tvw'
    PROCESSED_BUCKET = 'processed-bucket-tvw'
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    content = s3.get_object(Bucket=bucket, Key=key)['Body'].read()

    soup = BeautifulSoup(content, "html.parser")

    id_num = key.split('/')[-1].split('.')[0]
    
    job_title = soup.select_one('#titletextonly').contents
    job_title = ''.join(job_title)

    job_description = soup.select_one('#postingbody').contents
    job_description = ''.join(re.sub('^<br/>', '\n', str(line)) for line in job_description[2:])

    output[id_num] = {'title': job_title, 'description': job_description}

    s3.put_object(Body=json.dumps(output), Bucket=PROCESSED_BUCKET, Key=f'processed-{id_num}.json')
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
