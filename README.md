# Python-web-server
### Tested on Python 3.8

This webserver is BASIC. Do not hit it from multiple sophisticated browsers, and multiple machines.
It's meant for simple file get/put. It will likely timeout if under any significant load

curl or wget can be used to send files with options similar to the following:
```
  curl -X PUT --upload-file somefile.txt http://localhost:8000
  wget -O- --method=PUT --body-file=somefile.txt http://localhost:8000/somefile.txt
```
__Note__: curl automatically appends the filename onto the end of the URL so
the path can be omitted.

Base code from: https://floatingoctothorpe.uk/2017/receiving-files-over-http-with-python.html

Modified by Colby Burkett to:
```
    Allow for GET
    Eliminate lag on Windows due to address_string to a reverse lookup on the incoming IP
    Assign IP Port
```
