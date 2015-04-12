'''
Main entrypoint to the application.
'''

from models.imagedata import ImageData 
from deviantart.scraper import Scraper
from datastore.redis_store import RedisStore


import argparse
import signal
import sys

if __name__=="__main__":

    # Typical values are host = localhost, port = 6379, db = 0.
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str)
    parser.add_argument("--port", type=int)
    parser.add_argument("--db", type=int)

    args = parser.parse_args()
    host = args.host
    port = args.port
    db = args.db

    if None not in (host, port, db):
        # Persist to redis.
        redis_store = RedisStore(host, port, db, capacity=2000)

        def callback(image_data_items):
            for item in image_data_items:
                redis_store.add_image(item)
    else:
        def callback(image_data_items):
            for image_data in image_data_items:
                print image_data

    # Create a scraper.
    scraper = Scraper(callback, ping_interval=1)


    # Run the scraper.
    scraper.run()
