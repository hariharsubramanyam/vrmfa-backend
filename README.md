# vrmfa-scraper
Backend for the virtual reality museum for all

## Setup
The dependencies are specified in the `requirements.txt` file. You can install them automatically
if you install [`pip`](https://pip.pypa.io/en/stable/installing.html), which is a package manager for Python.

If you install pip, just run the following command (when in the directory containing `requirements.txt`).

`pip install -r requirements.txt`

## Usage
Simply run

`python main.py`

and the scraper will run, printing the scraped data to `stdout`.

You can also persist to a [**Redis**](http://redis.io/) cache. 

`python main.py --use-redis`

However, the script assumes a default host, port, and db for the Redis instance, so you may want
to tweak main accordingly (actually, these should be command line arguments). I'll implement
that later.

## Code Structure

* `requirements.txt` - Dependencies to install via `pip`
* `.gitignore` - List of files to omit from the Git repo (I use `virtualenv`, so I've ignored my `virtualenv` directory)
* `src/` - The source code
  * `main.py` - The main entry point of the application.
  * `models/` - Useful data structures
    * `imagedata.py` - Represents an image that can be placed in the museum.
  * `deviantart/` - Contains the logic for interacting with DeviantArt
    * `scraper.py` - Contains logic for running a scrape loop on a separate thread with periodically scrapes DeviantArt. 
    * `scrape.py` - **The actual scraping functionality**
  * `datastore` - Various datastores that the scraper can persist to.
    * `image_set.py` - An in-memory, threadsafe set of fixed capacity with random sampling and random eviction.
    * `redis_store.py` - Allow storing in Redis, a popular in-memory key-value store.
