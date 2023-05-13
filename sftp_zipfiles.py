import pysftp
import zipfile
import tempfile
import os
import re

from ftplib import FTP


def connect_sftp(hostname, username, password):
    sftp = FTP(hostname)
    sftp.login(user=username, passwd=password)

    return sftp


def get_files_by_pattern(sftp, patterns, remote_dir_path="/"):
    zip_files = []

    # get list of all zip files in remote dir
    # remote_files = sftp.listdir(remote_dir_path)
    remote_files = list(sftp.mlsd())
    # for each regex pattern:
    #    compile regex for case insensitive
    #    filter and get latest
    for raw_pattern in patterns:
        pattern = re.compile(raw_pattern, re.IGNORECASE)
        latest = sorted(
            filter(lambda v: re.findall(pattern, v[0]), remote_files), reverse=True
        )[0]
        zip_files.append(latest[0])

    return zip_files


# SFTP connection information
hostname = "ftp.imshealth.com.br"
username = "Colgate"
password = "43M94kBw"
patterns = [#r"FF_DDDMIX.+\d{6}_RERUN.zip",
            r"FF_MDTRMMIX_.+\d{6}_RERUN.zip"]


with connect_sftp(hostname, username, password) as sftp:
    match_files = get_files_by_pattern(sftp, patterns)
    # for f in match_files:
    #     print("Downloading: "+f)
    #     sftp.retrbinary("RETR " + match_files[0], open("/Users/andrew/Desktop/"+f, "wb").write
    #     )
    print(match_files)
# def zip_files_open(zip_files, remote_dir_path='/'):
#     with tempfile.TemporaryDirectory() as local_temp_path:
#         # iterate over zip files and download/extract them
#         for zip_file in zip_files:
#             # get last modified time of zip file on remote server
#             remote_file_path = sftp.normalize(os.path.join(remote_dir_path, zip_file))
#             # download zip file to local temp dir
#             local_temp_file_path = os.path.join(local_temp_path, zip_file)
#             sftp.get(remote_file_path, local_temp_file_path)

#             # extract files
#             with zipfile.ZipFile(local_temp_file_path) as zip_file:
#                 for member in zip_file.namelist():
#                     # write file to temp
#                     pass
