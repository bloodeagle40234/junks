from boto.s3.connection import S3Connection
from boto.exception import S3ResponseError
import boto
import logging
import os

logging.basicConfig(filename='s3.log', level=logging.DEBUG)

c = S3Connection(
    aws_access_key_id='swift:swift',
    aws_secret_access_key='swift',
    port=80,
    host='127.0.0.1',
    is_secure=False,
    debug=2,
    calling_format=boto.s3.connection.OrdinaryCallingFormat())


if __name__ == '__main__':
    bucket_name = 'test_tsuyu_mpupload'
    key_name = 'object'
    file_prefix = 'part'
    num_part = 3
    for suffix in xrange(1, 1 + num_part):
        os.system('dd if=/dev/zero of=%s bs=1M count=1' %
                  '.'.join([file_prefix, str(suffix)]))
    try:
        bucket = c.get_bucket(bucket_name)
    except S3ResponseError:
        bucket = c.create_bucket(bucket_name)

    mp = bucket.initiate_multipart_upload(key_name)
    for suffix in xrange(1, 1 + num_part):
        fp = open('.'.join([file_prefix, str(suffix)]))
        mp.upload_part_from_file(fp, suffix)
        fp.close()
    mp.complete_upload()
