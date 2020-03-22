# KVSS (Key-Value Storage Server)

This is a key-value server written in python 3, intended to implement 3 things:
  - store a string key with a string value __(/store/\<key\>:\<value\>)__
  - return a value if found __(/get/\<key\>)__
  - get a list of keys whose value start with a given string __(/find/\<string\>)__
  
(Everything is done thorugh HTTP GET requests.)
  
## Installing
Make sure you have python 3.8 installed. Unzip the the project. 
You're all set. No additional steps.

## Running the server
Run this command to see available options.
```bash
python main.py --help
```

TL;DL:\
use ``` --presistent <path_to_db>``` to store data on disk.

# Rationale
#### Not using dedicated framework:
First thing I considered was to use Flask. Even maybe Flask-RESTful,
but I figured it's a BIG overkill for a 3 function.

#### Not using proper http responses
The only reason to use Flask was to not have to worry about responses.
I could not justify that. Flask is small but not *that* small.
So to avoid working way too much for nothing, 418 will just have to do.

#### Using sqlite3
It ships with python...

#### Not using unittests.
Really needed to fit this project in 2 hours. 13 minutes left right now.

