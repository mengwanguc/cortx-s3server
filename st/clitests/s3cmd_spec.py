#!/usr/bin/python

from framework import Config
from framework import PyCliTest
from s3cmd import S3cmdTest
from jclient import JClientTest
from s3client_config import S3ClientConfig

# Helps debugging
# Config.log_enabled = True
# Config.dummy_run = True

# Set time_readable_format to False if you want to display the time in milli seconds.
# Config.time_readable_format = False

# TODO
# DNS-compliant bucket names should not contains underscore or other special characters.
# The allowed characters are [a-zA-Z0-9.-]*
#
# Add validations to S3 server and write system tests for the same.

#  ***MAIN ENTRY POINT

# Run before all to setup the test environment.
print("Configuring LDAP")
PyCliTest('Before_all').before_all()

# Set pathstyle =false to run jclient for partial multipart upload
S3ClientConfig.pathstyle = False
S3ClientConfig.access_key_id = 'AKIAJPINPFRBTPAYOGNA'
S3ClientConfig.secret_key = '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'

# Path style tests.
Config.config_file = "pathstyle.s3cfg"

# ************ Create bucket ************
S3cmdTest('s3cmd can create bucket').create_bucket("seagatebucket").execute_test().command_is_successful()

# ************ List buckets ************
S3cmdTest('s3cmd can list buckets').list_buckets().execute_test().command_is_successful().command_response_should_have('s3://seagatebucket')

# ************ 3k FILE TEST ************
S3cmdTest('s3cmd can upload 3k file').upload_test("seagatebucket", "3kfile", 3000).execute_test().command_is_successful()

S3cmdTest('s3cmd can download 3k file').download_test("seagatebucket", "3kfile").execute_test().command_is_successful().command_created_file("3kfile")

# ************ 8k FILE TEST ************
S3cmdTest('s3cmd can upload 8k file').upload_test("seagatebucket", "8kfile", 8192).execute_test().command_is_successful()

S3cmdTest('s3cmd can download 8k file').download_test("seagatebucket", "8kfile").execute_test().command_is_successful().command_created_file("8kfile")

# ************ OBJECT LISTING TEST ************
S3cmdTest('s3cmd can list objects').list_objects('seagatebucket').execute_test().command_is_successful().command_response_should_have('s3://seagatebucket/3kfile').command_response_should_have('s3://seagatebucket/8kfile')

S3cmdTest('s3cmd can list specific objects').list_specific_objects('seagatebucket', '3k').execute_test().command_is_successful().command_response_should_have('s3://seagatebucket/3kfile').command_response_should_not_have('s3://seagatebucket/8kfile')

# ************ DELETE OBJECT TEST ************
S3cmdTest('s3cmd can delete 3k file').delete_test("seagatebucket", "3kfile").execute_test().command_is_successful()

S3cmdTest('s3cmd can delete 8k file').delete_test("seagatebucket", "8kfile").execute_test().command_is_successful()

# ************ 700K FILE TEST ************
S3cmdTest('s3cmd can upload 700K file').upload_test("seagatebucket", "700Kfile", 716800).execute_test().command_is_successful()

S3cmdTest('s3cmd can download 700K file').download_test("seagatebucket", "700Kfile").execute_test().command_is_successful().command_created_file("700Kfile")

S3cmdTest('s3cmd can delete 700K file').delete_test("seagatebucket", "700Kfile").execute_test().command_is_successful()

# ************ 18MB FILE Multipart Upload TEST ***********
S3cmdTest('s3cmd can upload 18MB file').upload_test("seagatebucket", "18MBfile", 18000000).execute_test().command_is_successful()

S3cmdTest('s3cmd can download 18MB file').download_test("seagatebucket", "18MBfile").execute_test().command_is_successful().command_created_file("18MBfile")

S3cmdTest('s3cmd can delete 18MB file').delete_test("seagatebucket", "18MBfile").execute_test().command_is_successful()

# ************ Multiple Delete bucket TEST ************
file_name = "3kfile"
for num in range(0, 4):
  new_file_name = '%s%d' % (file_name, num)
  S3cmdTest('s3cmd can upload 3k file').upload_test("seagatebucket", new_file_name, 3000).execute_test().command_is_successful()

S3cmdTest('s3cmd can delete multiple objects').multi_delete_test("seagatebucket").execute_test().command_is_successful().command_response_should_have('delete: \'s3://seagatebucket/3kfile0\'').command_response_should_have('delete: \'s3://seagatebucket/3kfile3\'')

S3cmdTest('s3cmd should not have objects after multiple delete').list_objects('seagatebucket').execute_test().command_is_successful().command_response_should_not_have('3kfile')

# ************ Delete bucket TEST ************
S3cmdTest('s3cmd can delete bucket').delete_bucket("seagatebucket").execute_test().command_is_successful()

# ************ Signing algorithm test ************
S3cmdTest('s3cmd can create bucket nondnsbucket').create_bucket("nondnsbucket").execute_test().command_is_successful()
S3cmdTest('s3cmd can create bucket seagate-bucket').create_bucket("seagate-bucket").execute_test().command_is_successful()
S3cmdTest('s3cmd can create bucket seagatebucket123').create_bucket("seagatebucket123").execute_test().command_is_successful()
S3cmdTest('s3cmd can create bucket seagate.bucket').create_bucket("seagate.bucket").execute_test().command_is_successful()
S3cmdTest('s3cmd can delete bucket nondnsbucket').delete_bucket("nondnsbucket").execute_test().command_is_successful()
S3cmdTest('s3cmd can delete bucket seagate-bucket').delete_bucket("seagate-bucket").execute_test().command_is_successful()
S3cmdTest('s3cmd can delete bucket seagatebucket123').delete_bucket("seagatebucket123").execute_test().command_is_successful()
S3cmdTest('s3cmd can delete bucket seagate.bucket').delete_bucket("seagate.bucket").execute_test().command_is_successful()

# ************ Create bucket in region ************
S3cmdTest('s3cmd can create bucket').create_bucket("seagatebucket", "eu-west-1").execute_test().command_is_successful()

S3cmdTest('s3cmd created bucket in specific region').info_bucket("seagatebucket").execute_test().command_is_successful().command_response_should_have('eu-west-1')

S3cmdTest('s3cmd can delete bucket').delete_bucket("seagatebucket").execute_test().command_is_successful()


# Virtual Host style tests.
Config.config_file = "virtualhoststyle.s3cfg"

# ************ Create bucket ************
S3cmdTest('s3cmd can create bucket').create_bucket("seagatebucket").execute_test().command_is_successful()

# ************ List buckets ************
S3cmdTest('s3cmd can list buckets').list_buckets().execute_test().command_is_successful().command_response_should_have('s3://seagatebucket')

# ************ 3k FILE TEST ************
S3cmdTest('s3cmd can upload 3k file').upload_test("seagatebucket", "3kfile", 3000).execute_test().command_is_successful()

S3cmdTest('s3cmd can download 3k file').download_test("seagatebucket", "3kfile").execute_test().command_is_successful().command_created_file("3kfile")

# ************ 8k FILE TEST ************
S3cmdTest('s3cmd can upload 8k file').upload_test("seagatebucket", "8kfile", 8192).execute_test().command_is_successful()

S3cmdTest('s3cmd can download 8k file').download_test("seagatebucket", "8kfile").execute_test().command_is_successful().command_created_file("8kfile")

# ************ OBJECT LISTING TEST ************
S3cmdTest('s3cmd can list objects').list_objects('seagatebucket').execute_test().command_is_successful().command_response_should_have('s3://seagatebucket/3kfile').command_response_should_have('s3://seagatebucket/8kfile')

S3cmdTest('s3cmd can list specific objects').list_specific_objects('seagatebucket', '3k').execute_test().command_is_successful().command_response_should_have('s3://seagatebucket/3kfile').command_response_should_not_have('s3://seagatebucket/8kfile')

# ************ DELETE OBJECT TEST ************
S3cmdTest('s3cmd can delete 3k file').delete_test("seagatebucket", "3kfile").execute_test().command_is_successful()

S3cmdTest('s3cmd can delete 8k file').delete_test("seagatebucket", "8kfile").execute_test().command_is_successful()

# ************ 700K FILE TEST ************
S3cmdTest('s3cmd can upload 700K file').upload_test("seagatebucket", "700Kfile", 716800).execute_test().command_is_successful()

S3cmdTest('s3cmd can download 700K file').download_test("seagatebucket", "700Kfile").execute_test().command_is_successful().command_created_file("700Kfile")

S3cmdTest('s3cmd can delete 700K file').delete_test("seagatebucket", "700Kfile").execute_test().command_is_successful()

# ************ 18MB FILE Multipart Upload TEST ***********
S3cmdTest('s3cmd can multipart upload 18MB file').upload_test("seagatebucket", "18MBfile", 18000000).execute_test().command_is_successful()

S3cmdTest('s3cmd can download 18MB file').download_test("seagatebucket", "18MBfile").execute_test().command_is_successful().command_created_file("18MBfile")

S3cmdTest('s3cmd can delete 18MB file').delete_test("seagatebucket", "18MBfile").execute_test().command_is_successful()

#################################################

JClientTest('Jclient can upload partial parts to test abort and list multipart.').partial_multipart_upload("seagatebucket", "18MBfile", 18000000, 1, 2).execute_test().command_is_successful()

result = S3cmdTest('s3cmd can list multipart uploads in progress').list_multipart_uploads("seagatebucket").execute_test()
result.command_response_should_have('18MBfile')

upload_id = result.status.stdout.split('\n')[2].split('\t')[2]

result = S3cmdTest('S3cmd can list parts of multipart upload.').list_parts("seagatebucket", "18MBfile", upload_id).execute_test().command_is_successful()
assert len(result.status.stdout.split('\n')) == 4

S3cmdTest('S3cmd can abort multipart upload').abort_multipart("seagatebucket", "18MBfile", upload_id).execute_test().command_is_successful()

S3cmdTest('s3cmd can test the multipart was aborted.').list_multipart_uploads('seagatebucket').execute_test().command_is_successful().command_response_should_not_have('18MBfile')

############################################

# S3cmdTest('s3cmd can delete 18MB file').delete_test("seagatebucket", "18MBfile").execute_test().command_is_successful()
#
# S3cmdTest('s3cmd can abort multipart upload of 18MB file').multipartupload_abort_test("seagatebucket", "18MBfile", 18000000).execute_test(True).command_should_fail()
#
# S3cmdTest('s3cmd can list parts of multipart upload 18MB file').multipartupload_partlist_test("seagatebucket", "18MBfile", 18000000).execute_test().command_is_successful()
#
# S3cmdTest('s3cmd can delete 18MB file').delete_test("seagatebucket", "18MBfile").execute_test().command_is_successful()

# ************ Multiple Delete bucket TEST ************
file_name = "3kfile"
for num in range(0, 4):
  new_file_name = '%s%d' % (file_name, num)
  S3cmdTest('s3cmd can upload 3k file').upload_test("seagatebucket", new_file_name, 3000).execute_test().command_is_successful()

S3cmdTest('s3cmd can delete multiple objects').multi_delete_test("seagatebucket").execute_test().command_is_successful().command_response_should_have('delete: \'s3://seagatebucket/3kfile0\'').command_response_should_have('delete: \'s3://seagatebucket/3kfile3\'')

S3cmdTest('s3cmd should not have objects after multiple delete').list_objects('seagatebucket').execute_test().command_is_successful().command_response_should_not_have('3kfile')

# ************ Delete bucket TEST ************
S3cmdTest('s3cmd can delete bucket').delete_bucket("seagatebucket").execute_test().command_is_successful()

# ************ Signing algorithm test ************
S3cmdTest('s3cmd can create bucket seagate-bucket').create_bucket("seagate-bucket").execute_test().command_is_successful()
S3cmdTest('s3cmd can create bucket seagatebucket123').create_bucket("seagatebucket123").execute_test().command_is_successful()
S3cmdTest('s3cmd can create bucket seagate.bucket').create_bucket("seagate.bucket").execute_test().command_is_successful()
S3cmdTest('s3cmd can delete bucket seagate-bucket').delete_bucket("seagate-bucket").execute_test().command_is_successful()
S3cmdTest('s3cmd can delete bucket seagatebucket123').delete_bucket("seagatebucket123").execute_test().command_is_successful()
S3cmdTest('s3cmd can delete bucket seagate.bucket').delete_bucket("seagate.bucket").execute_test().command_is_successful()

# ************ Create bucket in region ************
S3cmdTest('s3cmd can create bucket').create_bucket("seagatebucket", "eu-west-1").execute_test().command_is_successful()

S3cmdTest('s3cmd created bucket in specific region').info_bucket("seagatebucket").execute_test().command_is_successful().command_response_should_have('eu-west-1')

S3cmdTest('s3cmd can delete bucket').delete_bucket("seagatebucket").execute_test().command_is_successful()

# ************ Collision Resolution TEST ************
S3cmdTest('s3cmd can create bucket').create_bucket("seagatebucket").execute_test().command_is_successful()
S3cmdTest('s3cmd can upload 3k file for Collision resolution test').upload_test("seagatebucket", "3kfile", 3000).execute_test().command_is_successful()

S3cmdTest('Deleted metadata using cqlsh for Collision resolution test').delete_metadata_test().execute_test().command_is_successful().command_is_successful()

S3cmdTest('Create bucket for Collision resolution test').create_bucket("seagatebucket").execute_test().command_is_successful()

S3cmdTest('s3cmd can upload 3k file after Collision resolution').upload_test("seagatebucket", "3kfile", 3000).execute_test().command_is_successful()

S3cmdTest('Check metadata have key 3kfile after Collision resolution').get_keyval_test().execute_test().command_is_successful().command_response_should_have('3kfile')

S3cmdTest('s3cmd can download 3kfile after Collision resolution upload').download_test("seagatebucket", "3kfile").execute_test().command_is_successful().command_created_file("3kfile")

S3cmdTest('s3cmd can delete 3kfile after collision resolution').delete_test("seagatebucket", "3kfile").execute_test().command_is_successful()

S3cmdTest('s3cmd can delete bucket').delete_bucket("seagatebucket").execute_test().command_is_successful()
