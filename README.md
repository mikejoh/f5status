# f5status
A very bulky script that fetches VS status from the F5 BIG-IP REST API and outputs the response in a colorful way. I will change the design of the script when i have time, 

# How-to get started
1. Download httplib2 via Python setuptools (pip)
2. Add your F5 LTM local API user (most often a user in the local user db) password to a file, i used a file called apipass.txt
3. Add your F5 environment and nodes in the f5status.conf file.
3. Run the command

$ python f5status.py --node lab01 --env LAB --user admin --password-from-file apipass.txt

# Other info
* Tested on TMOS version TMOS 11.6.x only, not 12.1.x with token based authentication to the API
* Tested in Python 2.7.2
* Requires httplib2
