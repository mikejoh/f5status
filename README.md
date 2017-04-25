# f5status
A script that fetches VS status from the F5 BIG-IP REST API and outputs the response in a colorful way. I will change the design of the script when i have time.

Required Python modules:
* `httplib2`

### Get started
1. Download httplib2 via Python setuptools (via pip or from your Linux distribution repo/Cygwin repo)
2. Add your F5 LTM local API user (most often a user in the local user db) password to a file, i used a file called `apipass.txt`
3. Add your F5 environment and nodes in the `f5status.conf` file
3. Run the command, see below for an example

```
$ f5status.py --node lab01 --env LAB --user admin --password-from-file apipass.txt
```
### Example config contents
```
[LAB]
lab01 = https://10.0.10.121

[PROD]
prod01 = https://192.168.0.1
```

### Other info
* Tested on TMOS version TMOS 11.6.x only, not 12.1.x with token based authentication to the API
* Tested in Python 2.7.2
* Tested in Cygwin
