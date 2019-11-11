### Necessary libraries:
pip install pySqsListener sqlite3 dateutil Flask webbrowser

### Necessary setup:
You'll need the following environment variables:
* AWS_ACCOUNT_ID

You'll need the following files:
~/.aws/config
> [default]
> region=eu-west-1

~/.aws/credentials
> [default]
> aws_access_key_id = <access key>
> aws_secret_access_key = <secret key>


### Running it
> python start.py

This will start the SQS listener as well as the webserver.
Additionally it will open a web browser to the map interface.


### Configuration
As this is a PoC, I left a lot of stuff inside the code.
For example:
- listener: (extra) filtering on BE
- listener: saving of the messages inside the cache directory (json format)
- use of SQLite instead of rds/mysql/...
- webservice: debug values outputted because no real data within the previous 3h
- webservice: mid-point based on OpenAQ's map for several different parameters
- webservice: port 5000
- start: name of region & sqs message queue
