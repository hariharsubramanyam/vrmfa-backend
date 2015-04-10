# vrmfa-backend
Backend for the virtual reality museum for all

## Setup
The dependencies are specified in the `requirements.txt` file. You can install them automatically
if you install [`pip`](https://pip.pypa.io/en/stable/installing.html), which is a package manager for Python.

If you install pip, just run the following command (when in the directory containing `requirements.txt`).

`pip install -r requirements.txt`


**Ignore this**
You can also persist the data in a PostgreSQL database. Make sure to install [PostgreSQL](http://www.postgresql.org/).

Create your database and user. Then, run

`python reset_db.py --dbname <your-database-name> --user <your-database-username>`

This will create the table **images** which will contain the images. Note that if the table already 
exists, it will be dropped.

## Usage
Simply run

`python main.py`

and the scraper will run, printing the scraped data to `stdout`.

**(still need to implement)**

If you're running the PostgreSQL database, you can persist the scraped data in the database.

`python main.py --dbname <your-database-name> --user <your-database-username>`

## Code Structure

* `requirements.txt` - Dependencies to install via `pip`
* `.gitignore` - List of files to omit from the Git repo (I use `virtualenv`, so I've ignored my `virtualenv` directory)
* `src/` - The source code
  * `main.py` - The main entry point of the application.
  * `reset_db.py` - Reset the database by dropping the tables used by the scraper and recreating them.
  * `models/` - Useful data structures
    * `imagedata.py` - Represents an image that can be placed in the museum.
  * `deviantart/` - Contains the logic for interacting with DeviantArt
    * `scraper.py` - Contains logic for running a scrape loop on a separate thread with periodically scrapes DeviantArt. 
    * `scrape.py` - **The actual scraping functionality**
  * `datastore` - Various datastores that the scraper can persist to.
    * `image_set.py` - An in-memory, threadsafe set of fixed capacity with random sampling and random eviction.
