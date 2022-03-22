import json
import boto3
import requests

host = 'https://search-photo-zb3hxahbrrsbcfgx2lryffue6i.us-east-1.es.amazonaws.com'
index = 'photo'
url = host + '/' + index + '/_doc'

awsauth = ('hando', '0912Namjoon!')
headers = { "Content-Type": "application/json" }

def lambda_handler(event, context):
    # TODO implement
    client=boto3.client('rekognition')

    # print(event)
    bucket = event['Records'][0]['s3']['bucket']['name']
    photo = event['Records'][0]['s3']['object']['key']
    # bucket = 'assign2-b2'
    # photo = "test5.jpg"
    reponse = client.detect_labels(Image={'S3Object':{'Bucket': bucket,'Name':photo}}, MaxLabels=10)['Labels']
    labels = []
    
    for label in reponse:
        labels.append(label['Name'])
    print("labels: ")
    print(labels)
    
    s3client = boto3.client('s3')
    metadata = s3client.head_object(
        Bucket=bucket,
        Key=photo,
    )
    
    print("meta:")
    print(metadata)
    
    # need to include custom labels from x-amz-meta-customLabels
    creation_time = metadata['LastModified'].isoformat()
    customLabels = metadata['ResponseMetadata']['HTTPHeaders']['x-amz-meta-customlabels'].split(",")
    
    print("creation time: ")
    print(creation_time)
    
    document = {
        "objectKey": photo,
        "bucket": bucket,
        "createdTimestamp": creation_time,
        "labels": labels+customLabels
    }
    print(document)
    
    r = requests.post(url, auth=awsauth, json=document, headers=headers)
    
    print("response: ")
    print(r)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
