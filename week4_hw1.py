from methods import *
import argparse

parser = argparse.ArgumentParser(
    description="CLI program that helps with uploading files on S3 buckets.",
    usage='''
    How to upload file:
    short:
        python week4_hw1.py -up -bn <bucket_name> -fn <file_path> 
    long:
       python week4_hw1.py --upload_file --bucket_name <bucket_name> --file_name <file_path>

    How to list buckets:
    short:
        python week4_hw1.py -lb
    long:
        python week4_hw1.py --list_buckets
    
    How to set versioning to a bucket:
    short:
         python week4_hw1.py -bn <bucket_name> -vers <Bool>
    long:
        python week4_hw1.py --bucket_name <bucket_name> --versioning <Bool>
        
    How to check objects version:
    short:
        python week4_hw1.py -bucket_name <bucket_name> -l_v -fn <file_path>
    long:
        python week4_hw1.py -bucket_name <bucket_name> -list_versions --file_name <file_path>
        
    How to delete old version of object:
    short:
        python week4_hw1.py -bn <bucket_name> -d_o_o_v
    long:
        python week4_hw1.py --bucket_name <bucket_name> --delete_old_objects_version  
    ''',
    prog='week4_hw1.py',
    epilog='hw1 and hw2')

parser.add_argument("-bn",
                    "--bucket_name",
                    type=str,
                    help="Pass bucket name.",
                    default=None)

parser.add_argument("-fn",
                    "--file_name",
                    type=str,
                    help="Pass file name.",
                    default=None)

parser.add_argument("-kfn",
                    "--keep_file_name",
                    help="Flag to keep original file name.",
                    choices=["False", "True"],
                    type=str,
                    nargs="?",
                    const="True",
                    default="False")

parser.add_argument("-lb",
                    "--list_buckets",
                    help="Flag to list bucket",
                    choices=["False", "True"],
                    type=str,
                    nargs="?",
                    const="True",
                    default="False")

parser.add_argument("-uf",
                    "--upload_file",
                    help="Flag to upload file",
                    choices=["False", "True"],
                    type=str,
                    nargs="?",
                    const="True",
                    default="False")

parser.add_argument("-vers",
                    "--versioning",
                    type=str,
                    help="list bucket object",
                    nargs="?",
                    default=None)

parser.add_argument("-l_v",
                    "--list_versions",
                    help="Flag to upload file",
                    choices=["False", "True"],
                    type=str,
                    nargs="?",
                    const="True",
                    default="False")

parser.add_argument("-d_o_o_v",
                    "--delete_old_objects_version",
                    help="Flag to upload file",
                    choices=["False", "True"],
                    type=str,
                    nargs="?",
                    const="True",
                    default="False")

s3_client = init_client()
args = parser.parse_args()
if s3_client:
    if args.bucket_name:
        if args.file_name and args.upload_file == "True":
            file_url = upload_local_file(s3_client, args.bucket_name, args.file_name, args.keep_file_name)
            print(file_url)

        if args.versioning == "True":
            versioning(s3_client, args.bucket_name, True)
            print(f"Enabled versioning on bucket {args.bucket_name}")

        if args.list_versions == "True":
            list_object_versions(s3_client, args.bucket_name, args.file_name)

        if args.delete_old_objects_version == "True":
            delete_old_version_or_object(s3_client, args.bucket_name)

    if args.list_buckets == "True":
        list_buckets(s3_client)

