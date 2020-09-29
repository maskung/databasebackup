#!/usr/bin/python
 
###########################################################
#
# This python script is used for mysql database backup
# using mysqldump and tar utility.
#
# Written by : Suphanut Thanyaboon
# Created date: Nov 09, 2020
# Last modified: Nov 10, 2020
# Tested with : Python 2.7.15 & Python 3.5
# Script Revision: 1.1
#
##########################################################
 
# Import required python libraries
 
import os
import time
import datetime
import pipes
import requests
import socket
 
# MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup.
# To take multiple databases backup, create any file like /backup/dbnames.txt and put databases names one on each line and assigned to DB_NAME variable.
 
DB_HOST = 'localhost' 
DB_USER = 'root'
DB_USER_PASSWORD = 'password'
DB_NAME = '/var/root/backup_program/dblist.txt'
#DB_NAME = 'cotto'
BACKUP_PATH = '/var/root/backup'
 
# Getting current DateTime to create the separate backup folder like "20180817-123433".
DATETIME = time.strftime('%Y%m%d-%H%M%S')
TODAYBACKUPPATH = BACKUP_PATH + '/' + DATETIME
 
# Checking if backup folder already exists or not. If not exists will create it.
try:
    os.stat(TODAYBACKUPPATH)
except:
    os.mkdir(TODAYBACKUPPATH)
 
# Code for checking if you want to take single database backup or assinged multiple backups in DB_NAME.
print ("checking for databases names file.")
if os.path.exists(DB_NAME):
    file1 = open(DB_NAME)
    multi = 1
    print ("Databases file found...")
    print ("Starting backup of all dbs listed in file " + DB_NAME)
else:
    print ("Databases file not found...")
    print ("Starting backup of database " + DB_NAME)
    multi = 0
 
# Starting actual database backup process.
if multi:
   in_file = open(DB_NAME,"r")
   flength = len(in_file.readlines())
   in_file.close()
   p = 1
   dbfile = open(DB_NAME,"r")
 
   db_display = ""
   while p <= flength:
       db = dbfile.readline()   # reading database name from file
       db = db[:-1]         # deletes extra line
       dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
       os.system(dumpcmd)
       gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
       os.system(gzipcmd)
       db_display += db + ".sql.gz --> " + str(round(os.path.getsize(pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql.gz")/(1024*1024),2)) +  " M\n"
       #print (os.path.getsize(pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql.gz"))
       p = p + 1
   dbfile.close()
else:
   db = DB_NAME
   dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
   os.system(dumpcmd)
   gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
   os.system(gzipcmd)
 
#print ("")
#print ("Backup script completed")
#print ("Your backups have been created in '" + TODAYBACKUPPATH + "' directory")
#caculate free filesytem size
def disk_usage(path):
        """Return disk usage statistics about the given path.

        Returned value is a named tuple with attributes 'total', 'used' and
        'free', which are the amount of total, used and free space, in bytes.
        """
        st = os.statvfs(path)
        free = st.f_bavail * st.f_frsize
        total = st.f_blocks * st.f_frsize
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        return (total, used, free)

total, used, free  = disk_usage('/')
#print (str(round((total/(1024*1024*1024)))) + "G\n")
#print (str(round((used/(1024*1024*1024)))) + "G\n")
#print (str(round((free/(1024*1024*1024)))) + "G\n")
text_display = "backup complete on " + socket.gethostname() + "\n"
text_display += "Your backups created in '" + TODAYBACKUPPATH + "/' " + "\n"
text_display += db_display
text_display += "Disk avaliable : " + str(round((free/(1024*1024*1024)))) + "G(" + str(round((free/used)*100)) + "%)\n"

print (text_display)

#send to Line API
url = 'https://notify-api.line.me/api/notify'
#1-on-1 notifiy
token = 'mIo9LwELT1TjOkajPk4AaN35K1T2VeULc9vgC63IhfC'
#admin group
#token = '1e0kAIyAkhwnMDMJ4iwKFYciexjcujsX9rJp3g6r9ba'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

msg =  text_display
r = requests.post(url, headers=headers, data = {'message':msg})
