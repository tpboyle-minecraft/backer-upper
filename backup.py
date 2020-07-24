
#
# Requires
#   Python 3.5+
#   packages:
#     - ftputil
#     - selenium
#


##  IMPORTS  ##

from datetime import datetime
from ftplib import FTP
from pathlib import Path
import ftputil
import glob
import os
import selenium
import shutil
import zipfile


##  LOCAL IMPORTS  ##

import connection as conn  
    # IMPORTANT: you must define this file.
    # It provides the following variables:
    #    ip
    #    ftp_username
    #    ftp_password
    #    remote_port
    # These are used to connect to the remote FTP host.
    # ! >>  stopstart.py has some additional variables that need to be set.
    # .gitignored by default because this needs to be set up by the user.


##  CONFIG  ##

# BASIC
local_backups_dir = "./backups"

# ADVANCED
buf_size = 1024     # num bytes to send at a time
tmp_dir = ".tmp"


##  CONSTANTS  ##

MONTHS = {
    1: '01_Jan',
    2: '02_Feb',
    3: '03_Mar',
    4: '04_Apr',
    5: '05_May',
    6: '06_Jun',
    7: '07_Jul',
    8: '08_Aug',
    9: '09_Sep',
    0: '10_Oct',
    1: '11_Nov',
    2: '12_Dec',
}


## MAIN ##

def backup():
    global tmp_dir
    # Locally create backup folder.
    curr_backup_dir = get_curr_backup_dir()
    curr_backup_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir = os.path.join(str(curr_backup_dir), tmp_dir)
    # Download world/ file & zip.
    #   I do this all three times so if there are any errors
    #    with one backup there are others to replace it.
    for i in range(1,4):
        create_backup(curr_backup_dir, i)

def create_backup(dest, name):
    delete_tmp()  # ensure there's no tmp dir
    download_to_tmp()
    zip_tmp_to(dest, name)
    delete_tmp()


##  CURRENT BACKUP DIRECTORY  ##

def get_curr_backup_dir():
    year, month, day = get_curr_date()
    curr_time = str(get_curr_time())
    curr_backup_dir_str = os.path.join(
        local_backups_dir,
        year,
        get_month_shorthand(month),
        day,
        curr_time
    )
    curr_backup_dir = Path(curr_backup_dir_str)
    return curr_backup_dir

def get_curr_date():
    curr_date_str = str(datetime.date(datetime.now()))
    curr_date = curr_date_str.split('-')
    year = curr_date[0]
    month = curr_date[1]
    day = curr_date[2]
    return year, month, day

def get_curr_time():
    curr_time = str(datetime.time(datetime.now()))
    curr_time = curr_time[:5]   # cut seconds & microseconds
    curr_time = curr_time.replace(":", "-")
    return curr_time

def get_month_shorthand(month_num):
    return MONTHS[int(month_num)]


##  TMP  ##

def delete_tmp():
    tmp_dirs = glob.glob(tmp_dir + "*")
    for tmp in tmp_dirs:
        shutil.rmtree(tmp)


##  FTP  ##

def download_to_tmp():
    ftp, ftp_host = setup_ftp()
    if(not os.path.exists(tmp_dir)):
        os.mkdir(tmp_dir)
    for root, _, files in ftp_host.walk('world/', topdown=True):
        local_dir = os.path.join(tmp_dir, root)
        if(not os.path.exists(local_dir)):
            os.mkdir(local_dir)
        for file in files:
            remote_file = os.path.join(root, file).replace('\\', '/')
            local_file = os.path.join(local_dir, file)
            with open(local_file, "wb") as fp:
                ftp.retrbinary('RETR ' + remote_file, fp.write, buf_size)
    # Cleanup.
    ftp.quit()
    ftp_host.close()

def setup_ftp():
    ftp = FTP(
        host = conn.ip,
        user = conn.ftp_username,
        passwd = conn.ftp_password
    )
    ftp_host = ftputil.FTPHost(
        conn.ip,
        conn.ftp_username,
        conn.ftp_password
    )
    return ftp, ftp_host


##  ZIP  ##

def zip_tmp_to(backup_dir, zip_name):
    local_dest_zip = os.path.join(backup_dir, str(zip_name) + '.zip')
    cwd = os.getcwd()
    os.chdir(tmp_dir)
    zip_dir("world/", os.path.join(cwd, local_dest_zip))
    os.chdir(cwd)

# https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory-in-python
def zip_dir(ori, des):
    ziph = zipfile.ZipFile(des, mode='w')
    try:
        for root, dirs, files in os.walk(ori):
            for file in files:
                ziph.write(os.path.join(root, file))
    finally:
        ziph.close()

