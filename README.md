# vrmfa-backend
Backend for the virtual reality museum for all

## Setup
The dependencies are specified in the `requirements.txt` file. You can install them automatically
if you install [`pip`](https://pip.pypa.io/en/stable/installing.html), which is a package manager for Python.

If you install pip, just run the following command (when in the directory containing `requirements.txt`).

`pip install -r requirements.txt`

You should also make sure you have [**Redis**](http://redis.io/).

## Usage
Data is persisted in a [**Redis**](http://redis.io/) cache. 

To run the scraper, run

`python run_scraper.py --host <host> --port <port> --db <db>`

Where the host, port number, and database number are specified for the Redis cache. If you omit them,
the scraper will just print to `stdout`.

To run the server (which provides the API), run

`python server.py --host <host> --port <port> --db <db>`

Where host, port, and database number are specified for the Redis cache. If you omit them, the server
won't run.

## Code Structure

TODO: Update this
