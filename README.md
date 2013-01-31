twitter-followers
=================

Python based script to get twitter followers and output to a csv file


How to use
----------
1. Install python and all packages
The order is: Python (then set PATH and open a CMD window), setuptools (Windows installer, if not in Windows, you need to find a similar tool), httplib2 (python package), oauth2 (python package).

2. If required, set up a proxy. Skip this step if you are not using proxy.
In Command window type:
```
set http_proxy
```
If empty or not correct, set the value manually.
To set environment variable permanently, change it in system settings.
Alternatively, in individual session,
```
set http_proxy="http://proxy.company.com:3128"
```
in command window.

3. Run program  
Change to project folder, type
```
python followers.py start_number to_number
```
start_number: from this follower number in twitter's own order.
start_number: to this follower number in twitter's own order.
For example,
```
python followers.py 1 100 -- export the first 100 followers
```
```
python followers.py 101 1000 -- export follower 101 to 1000
```
```
python followers.py 1 100000 -- export all followers (if the total number is less than 100000).
```
It might fail. See below for explaination.


Twitter's restrictions
----------------------
Due to Twitter's restrictions, up to around 1000 followers may be populated in a short time. Twitter allows up to 150 API calls per hour (up to 100 followers can be retrieved in one call. For example to get 250 followers will invoke 3 calls). Plus running the program itself will invoke one call thus the program needs to split the followers when there are too many of them. 


Copyright
---------
This Python script is free to modify, use and distribute. 3rd party tools has their own copyright information. Please read them carefully before use.

