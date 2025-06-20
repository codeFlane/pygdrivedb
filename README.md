# pygdrivedb
Upload xml and db file from traccar to Google Drive storage.
Do backup every day at 04:00 by Dallas timezone.

## procedure of actions
1. google drive auth
2. wait for 04:00
3. making archive that contains db and xml file
4. upload archive to google drive
5. remove old files (google drive storage must contain only 3 archives for last 3 days)
6. repeat from 2nd step

## requirements
all requirements in req.txt file
google-api-python-client, google-auth-httplib2, google-auth-oauthlib - google drive client library
simple-scheduler - scheduler
