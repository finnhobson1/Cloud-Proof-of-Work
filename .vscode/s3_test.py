import boto3

s3 = boto3.resource('s3')
bucket = s3.Bucket('fh16413-pow-bucket')
key = 'output'
objs = list(bucket.objects.filter(Prefix=key))

if len(objs) > 0:
    objs[0].delete()