#construction of and s3 bucket and a cloudformation distribution.
import boto3
import uuid

region = 'eu-west-1'
s3client = boto3.client('s3', region_name=region)
cfclient = boto3.client('cloudfront')
location = {'LocationConstraint': region}

#create bucket.
bucket_name = 'python-sdk-sample-{}'.format(uuid.uuid4())
print('Creating new bucket with name: {}'.format(bucket_name))
s3client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

#create/put object.
object_key = 'index.html'
s3client.put_object(Bucket=bucket_name, Key=object_key, Body=b'<html><head><title>My First Webpage</title></head><body><h1>I love coffee</h1><p>Hello world!</p></body></html>')

#enable static ws hosting
# website_configuration = {
#     'ErrorDocument': {'Key': 'error.html'},
#     'IndexDocument': {'Suffix': 'index.html'},
# }
# s3client.put_bucket_website(Bucket=bucket_name,
#                       WebsiteConfiguration=website_configuration)

#generate url to preview
url = s3client.generate_presigned_url(
    'get_object', {'Bucket': bucket_name, 'Key': object_key})
print('\nTry this URL in your browser to download the object:')
print(url)
input("\nPress enter to continue...")

#create cloudfront
origin_domain = '.'.join([bucket_name, "s3.eu-west-1.amazonaws.com"])
print("--> "+origin_domain)
origin = {'Quantity': 1, 'Items': [{'Id': '1', 'DomainName': origin_domain, 'S3OriginConfig': {'OriginAccessIdentity': ''}}]}
distribution_config = {
        'CallerReference': str(uuid.uuid4()),
        'Origins': origin,
        'Comment': 'hello',
        'DefaultRootObject': 'index.html',
        'Enabled': True,
        'DefaultCacheBehavior': {
                'TargetOriginId': '1',
                'ViewerProtocolPolicy': 'allow-all',
                'MinTTL': 1000,
                'TrustedSigners': dict(Quantity=0, Enabled=False),
                'ForwardedValues': dict(Cookies = {'Forward': 'all'}, Headers = dict(Quantity=0), QueryString=False, QueryStringCacheKeys= dict(Quantity=0))
                }
        }
res = cfclient.create_distribution(DistributionConfig = distribution_config)

input("\nPress enter to continue...")

#delete resources
# cfclient.delete_ditribution(Id = res['Distribution']['Id'])
# s3client.delete_object(Bucket = bucket_name, Key = object_key)
# s3client.delete_bucket(Bucket= bucket_name)
