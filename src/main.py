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
    parser = argparse.ArgumentParser()
    parser.add_argument("--use-redis", dest="use_redis", action="store_true")

    args = parser.parse_args()

    if args.use_redis:
        # Persist to redis.
        redis_store = RedisStore('localhost', 6379, 0, capacity=2000)

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

    print "Type any value (and enter) to quit"
    val = raw_input()
    scraper.stop()
