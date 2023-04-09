import magic
from hashlib import md5
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
import logging
import datetime
from os import getenv
from dotenv import load_dotenv

load_dotenv()

def init_client():
    try:
        client = boto3.client("s3",
                              aws_access_key_id = getenv("aws_access_key_id"),
                              aws_secret_access_key = getenv("aws_secret_access_key"),
                              aws_session_token = getenv("aws_session_token"),
                              region_name = getenv("aws_region_name"))
        client.list_buckets()
        return client
    except ClientError as e:
        logging.error(e)
    except:
        logging.error(("Unexpected error"))



def generate_file_name(file_name) -> str:
    file_extension = file_name.split('.')[-1]
    return f'up_{md5(str(datetime.now()).encode("utf-8")).hexdigest()}.{file_extension}'


def upload_local_file(aws_s3_client, bucket_name, filename, keep_file_name=False):
    mime = magic.Magic(mime=True)
    content_type = mime.from_file(filename)
    print(content_type)
    file_name = filename.split('/')[-1] if keep_file_name else generate_file_name(filename.split('/')[-1])
    print(file_name)
    try:
        aws_s3_client.upload_file(filename, bucket_name, file_name, ExtraArgs={'ContentType': content_type})

        return f"https://{bucket_name}.s3.{getenv('aws_region_name')}.amazonaws.com/{file_name}"

    except ClientError as e:
        logging.error(e)
    except Exception as ex:
        logging.error(ex)

    return False

def list_buckets(aws_s3_client):
    try:
        buckets = aws_s3_client.list_buckets()
        if buckets:
            for bucket in buckets['Buckets']:
                print(f"    {bucket['Name']}")

    except ClientError as e:
        logging.error(e)



def versioning(aws_s3_client, bucket_name, status : bool):
    versioning_status = "Enabled" if status else "Suspended"
    aws_s3_client.put_bucket_versioning(
        Bucket=bucket_name,
        VersioningConfiguration={
            "Status": versioning_status
        }
    )


def list_object_versions(aws_s3_client, bucket_name, file_name):
    versions = aws_s3_client.list_object_versions(
        Bucket=bucket_name,
        Prefix=file_name
    )

    # print(versions)
    for version in versions['Versions']:
        version_id = version['VersionId']
        file_key = version['Key'],
        is_latest = version['IsLatest']
        modified_at = version['LastModified']

        print(version_id, file_key, is_latest, modified_at)


def delete_old_version_or_object(aws_s3_client, bucket_name):
    current_date = datetime.datetime.now(datetime.timezone.utc)

    versions = aws_s3_client.list_object_versions(Bucket=bucket_name)['Versions']

    for version in versions:
        creation_date = version['LastModified']
        age = current_date - creation_date

        if age > datetime.timedelta(days=180):
            aws_s3_client.delete_object(Bucket=bucket_name, Key=version['Key'], VersionId=version['VersionId'])
