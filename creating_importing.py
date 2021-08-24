import boto3
import uuid
import yaml


#param
region = 'eu-west-1'
s3client = boto3.client('s3', region_name=region)
cfclient = boto3.client('cloudfront')
cf0client = boto3.client('cloudformation')
location = {'LocationConstraint': region}

#creating bucket
bucket_name = 'python-sdk-sample-{}'.format(uuid.uuid4())
print('Creating new bucket with name: {}'.format(bucket_name))
# s3client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
input("\nPress enter to continue...")

#creating CloudFront distribution
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
# res = cfclient.create_distribution(DistributionConfig = distribution_config)
input("\nPress enter to continue...")

#adding to CloudFormation Template
s3_tem_name = 'S3Bucket' + bucket_name[30] + bucket_name[27] + bucket_name[20]
print(s3_tem_name + ' ' + bucket_name)
cf_tem_name = 'CloudFrontDistribution' + bucket_name[30] + bucket_name[27] + bucket_name[20]
toAdd = {
        s3_tem_name: {
           'Type': 'AWS::S3::Bucket',
           'DeletionPolicy': 'Retain',
           'Properties': {
           'BucketName': bucket_name
           }
        },
        # cf_tem_name: {
        #  'Type': 'AWS::CloudFront::Distribution',
        #  'DeletionPolicy': 'Retain',
        #  'Properties': {
        #      'DistributionConfig': {
        #         'Origins': [
        #             {
        #             'ConnectionAttempts': 3,
        #             'ConnectionTimeout': 10,
        #             'DomainName': origin_domain,
        #             'Id': '1', 'OriginPath': '',
        #             'S3OriginConfig': {
        #                'OriginAccessIdentity': ''
        #                }
        #             }
        #             ],
        #         'OriginGroups': {'Quantity': 0},
        #         'DefaultCacheBehavior': {
        #            'AllowedMethods': ['HEAD', 'GET'],
        #            'CachedMethods': ['HEAD', 'GET'],
        #            'Compress': False,
        #            'DefaultTTL': 86400,
        #            'ForwardedValues': {'Cookies': {'Forward': 'all'},'QueryString': False},
        #            'MaxTTL': 31536000,
        #            'MinTTL': 1000,
        #            'SmoothStreaming': False,
        #            'TargetOriginId': '1',
        #            'ViewerProtocolPolicy': 'allow-all'
        #         },
        #         'Comment': 'hello',
        #         'PriceClass': 'PriceClass_All',
        #         'Enabled': True,
        #         'ViewerCertificate': {'CloudFrontDefaultCertificate': True, 'MinimumProtocolVersion': 'TLSv1'},
        #         'Restrictions': {'GeoRestriction': {'RestrictionType': 'none'}},
        #         'HttpVersion': 'http2',
        #         'DefaultRootObject': 'index.html',
        #         'IPV6Enabled': True}}}
            }
with open('cf_template_sdk.yml') as file:
    data = yaml.safe_load(file)
data['Resources'] = data['Resources'] | toAdd

with open('cf_template_sdk.yml', 'w') as file:
    docs = yaml.dump(data, file)

#Ajout au CloudFormation Stack
# resultat = cf0client.create_change_set(
#       StackName = 'arn:aws:cloudformation:eu-west-1:585831369267:stack/demoStack/f48679e0-04dd-11ec-b5c0-0660dabef07f',
#       TemplateBody = yaml.dump(data),
#       ChangeSetName = 'demoChangeSet',
#       ChangeSetType = 'UPDATE',
      # ResourcesToImport = [
      #   {
      #   'ResourceType': 'AWS::S3::Bucket',
      #   'LogicalResourceId': s3_tem_name,
      #   'ResourceIdentifier': {'BucketName': bucket_name},
      #   },
      #   {
      #   'ResourceType': 'AWS::CloudFront::Distribution',
      #   'LogicalResourceId': cf_tem_name,
      #   'ResourceIdentifier': {'Id': res['Distribution']['Id']}
      #   }
      #   ,{
      #   'ResourceType': 'AWS::S3::Bucket',
      #   'LogicalResourceId': 'S3Bucket',
      #   'ResourceIdentifier': {'BucketName': 'python-sdk-sample-c9492900-7745-42cf-9ba2-cec6ef3d9c10'}
      #   },
      #   {
      #   'ResourceType': 'AWS::CloudFront::Distribution',
      #   'LogicalResourceId': 'CloudFrontDistribution',
      #   'ResourceIdentifier': {'Id': 'E1XAAWFGBLPVO3'}
      #   }
      # ]
# )
helllo = cf0client.list_stacks(StackStatusFilter = ['CREATE_IN_PROGRESS','CREATE_FAILED','CREATE_COMPLETE'])
print(helllo)
