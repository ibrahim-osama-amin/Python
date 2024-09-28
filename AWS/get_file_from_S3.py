import boto3
import botocore
s3 = boto3.client('s3')
s3_objects = s3.list_objects(Bucket='papita-dota')

s3_contents = s3_objects['Contents']

#print(s3_contents)
for i in s3_contents:
    if i['Key'] == "coffee.jpg":
        print(i['Key'])