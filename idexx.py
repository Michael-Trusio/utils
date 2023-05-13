import pandas as pd
import datetime
import pysftp

import zipfile
import tempfile
import os
import re


def connect_sftp(hostname, username, password):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    sftp = pysftp.Connection(
        host=hostname, username=username, password=password, cnopts=cnopts
    )

    return sftp

def get_zip_files_by_pattern(sftp, patterns, remote_dir_path = "/"):
    zip_files = []

    # get list of all zip files in remote dir
    remote_files = sftp.listdir(remote_dir_path)

    # for each regex pattern:
    #    compile regex for case insensitive
    #    filter and get latest
    for raw_pattern in patterns:
        pattern = re.compile(raw_pattern,re.IGNORECASE)
        latest = sorted(filter(lambda v: re.match(pattern, v), remote_files), reverse=True)[0]
        zip_files.append(latest)

    return zip_files

# SFTP connection information
hostname = "ftp.imshealth.com.br"
username = "Colgate"
password = "43M94kBw"
patterns = [r'FF_DDDMIX.+\d{6}.zip', r'FF_MDTRMMIX_OPEN_CHANNELS.+\d{6}.zip']


with connect_sftp(hostname, username, password) as sftp:
    zip_files = get_zip_files_by_pattern(sftp, patterns)

    # temp directory created
def zip_files_open(zip_files, tempfile):
    with tempfile.TemporaryDirectory() as local_temp_path:
        # iterate over zip files and download/extract them
        for zip_file in zip_files:
            # get last modified time of zip file on remote server
            remote_file_path = sftp.normalize(os.path.join(remote_dir_path, zip_file))
            remote_modified_time = sftp.stat(remote_file_path).st_mtime
            modified_time = datetime.datetime.fromtimestamp(remote_modified_time).strftime(
            "%Y-%m-%d %H:%M"
            )

            # check if zip file was modified between certain dates
            if (
                    start_date
                    <= datetime.datetime.fromtimestamp(remote_modified_time)
                    <= end_date
            ):
                # download zip file to local temp dir
                local_temp_file_path = os.path.join(local_temp_path, zip_file)
                sftp.get(remote_file_path, local_temp_file_path)

                # extract CSV files
                with zipfile.ZipFile(local_temp_file_path) as zip_file:
                    for member in zip_file.namelist():
                        if member.endswith(".csv"):
                            df = pd.read_csv(
                                zip_file.open(member), low_memory=False, dtype="object"
                            )
                            # rename all columns to upper case and take out all commas
                            df = df.rename(columns=str.upper)
                            df = df.replace(",", "", regex=True)
                            # add new columns in the DataFrame
                            df["FILE_MODIFIED_DATE"] = modified_time
                            df["EXTRACTED_FROM"] = member
                            df["ETRACTED_WHEN"] = pd.Timestamp.today().strftime("%Y-%m-%d")
                            # data csv
                            df.to_csv(
                                f"C:\\Users\\john.mcgraw\\Documents\\Hills_US\\Idexx_Testing\\{member}",
                                sep="|",
                                index=False,
                            )
