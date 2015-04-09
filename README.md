# vrmfa-backend
Backend for the virtual reality museum for all

## Setup
The dependencies are specified in the `requirements.txt` file. You can install them automatically
if you install [`pip`](https://pip.pypa.io/en/stable/installing.html), which is a package manager for Python.

If you install pip, just run the following command (when in the directory containing `requirements.txt`).

`pip install -r requirements.txt`

You can also persist the data in a PostgreSQL database. Make sure to install [PostgreSQL](http://www.postgresql.org/).

Create your database and user. Then, run

`python reset_db.py --dbname <your-database-name> --user <your-database-username>`

This will create the table **images** which will contain the images. Note that if the table already 
exists, it will be dropped.

## Usage
Simply run

`python main.py`

and the scraper will run, printing the scraped data to `stdout`.

(still need to implement).
If you're running the PostgreSQL database, you can persist the scraped data in the database.

`python main.py --dbname <your-database-name> --user <your-database-username>`
