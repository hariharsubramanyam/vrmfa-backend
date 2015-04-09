from deviantart.scrape import ScrapeImplementation

import time
import threading

'''
The web scraper which pulls image data from DeviantArt.
'''
class Scraper:
    '''
    Create the scraper.

    @param callback - The function to execute after each chunk of image data has been retrieved. 
                      The callback should accept a list of ImageData instances. The scraper does
                      not handle de-duplication, so the callback should.
    @param ping_interval - The number of seconds to wait before pinging the website again.
    '''
    def __init__(self, callback, ping_interval=25):
        self.callback = callback
        self.ping_interval = ping_interval

        # We want to avoid the current thread and the scrape loop thread from modifying the
        # thread_running and ticks_until_next_scrape variables at the same time.
        # So, they'll acquire this mutex before the modify, and they'll release it when they're done.
        self.mutex = threading.Lock()

        # When false, the scrape loop will terminate (and thus its thread will terminate).
        self.thread_running = False

        # The thread running the loop for the scraper.
        self.thread = threading.Thread(target=self.scrape_loop)

        # The scrape loop runs every second (a tick). This is the number of ticks it must
        # wait until it can scrape DeviantArt again.
        self.ticks_until_next_scrape = ping_interval

        # Create the implementation object which performs the scraping.
        self.scrape_implementation = ScrapeImplementation()


    '''
    The loop that will scrape periodically.
    '''
    def scrape_loop(self):
        while True:
            # Check if we should return (and therefore kill the thread).
            if not self.is_thread_running():
                return

            # Determine if we should scrape on this tick.
            self.tick()
            if self.should_scrape():
                # Scrape the images and trigger the callback.
                images_data_items = self.scrape_implementation.scrape()
                self.callback(images_data_items)
            time.sleep(1)

    '''
    Run the scraper. This will launch another thread, so make sure to terminate it by calling
    stop().
    '''
    def run(self):
        if self.is_thread_running():
            return
        self.set_thread_running(True)
        self.reset_ticks_until_scrape()
        self.thread.start()

    '''
    Kill the scraper, if it is currently running.
    '''
    def stop(self):
        self.mutex.acquire()
        self.thread_running = False
        self.mutex.release()

    '''
    Reset the number of ticks needed until the next scrape (while holding the mutex).
    '''
    def reset_ticks_until_scrape(self):
        self.mutex.acquire()
        self.ticks_until_next_scrape = self.ping_interval
        self.mutex.release()

    '''
    Decrement the ticks_until_next_scrape when the mutex is acquired.
    '''
    def tick(self):
        self.mutex.acquire()
        self.ticks_until_next_scrape -= 1
        self.mutex.release()

    '''
    @return Whether we need to scrape on this tick (check while holding the mutex).
    '''
    def should_scrape(self):
        self.mutex.acquire()
        ticks_until_scrape = self.ticks_until_next_scrape
        self.mutex.release()
        return ticks_until_scrape <= 0

    '''
    Acquire the mutex and check whether the scrape loop thread is running.
    @return - Whether the scrape loop thread is running.
    '''
    def is_thread_running(self):
        self.mutex.acquire()
        thread_running = self.thread_running
        self.mutex.release()
        return thread_running

    '''
    Set whether the thread is running.
    @param new_value - whether the thread is running (True or False).
    '''
    def set_thread_running(self, new_value):
        self.mutex.acquire()
        self.thread_running = new_value
        self.mutex.release()

    '''
    Return string representation of this object.
    '''
    def __repr__(self):
        return "Scraper(ping_interval=%d)" % (self.ping_interval,)