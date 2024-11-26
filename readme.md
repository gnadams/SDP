
# API for network metrics

This is hosted for free with Render, at https://computernetworks-project.onrender.com/ 

Due to limitations for the free hosting version, the site will go inactive after 30 minutes. While inactive, the site will take 2-3 minutes to load.

See https://computernetworks-project.onrender.com/docs for api documentation


## Purpose
The goal is to have my local host periodically gather the bandwidth of my home internet, and then upload it to the cloud via a POST request.

## Project Layout
### SQLite
Each Bandwidth upload is stored in the <b>sql_app.db</b>

The sql_app directory contains all the models/schemas for managing/interacting with the database.

### FastAPi
The fastAPI framework and methods are launched in <b>main.py</b>

The 2 important GET requests are:

<b>GET</b> /Recent/ (The most recent bandwidth)

 and

 <b>GET</b> /recentBandwidths/
(The last X Bandiwdth objects)


### LocalHostFiles
This directory contains <b>test.py</b>, and <b>loop.py</b>

Loop.py will be ran on the local host to transmit the bandwidth data to the hosted application via a post request at:
https://computernetworks-project.onrender.com/upload/



## How to run locally?

run 
```
pip install -r requirements.txt
```
and
```
uvicorn main:app --reload
```

