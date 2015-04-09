import time
import threading

'''
The web scraper which pulls image data from DeviantArt.
'''
class Scraper:
    '''
    Create the scraper.

    @param callback - The function to execute after each chunk of image data has been retrieved. 
                      The callback should accept a list of ImageData instances. It will not be called
                      with the same ImageData instance twice.
    @param ping_interval - The number of seconds to wait before pinging the website again.
    @param max_imagedata_in_mem - The maximum number of ImageData instances that the scraper will be allowed 
                       to store in memory.
    '''
    def __init__(self, callback, ping_interval=25, max_imagedata_in_mem=1000):
        self.callback = callback
        self.ping_interval = ping_interval
        self.max_imagedata_in_mem = max_imagedata_in_mem

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


    '''
    The loop that will scrape periodically.
    '''
    def scrape_loop(self):
        while True:
            # Check if we should return (and therefore kill the thread).
            self.mutex.acquire()
            if not self.thread_running:
                self.mutex.release()
                return

            # Determine if we should scrape on this tick.
            self.ticks_until_next_scrape -= 1
            if self.ticks_until_next_scrape == 0:
                shouldScrape = True
                self.ticks_until_next_scrape = self.ping_interval
            else:
                shouldScrape = False
            self.mutex.release()

            # Scrape if needed, then sleep until the next tick.
            if shouldScrape:
                self.scrape()
            time.sleep(1)

    '''
    Scrape DeviantArt, parse the HTML to get the list of ImageData, and then call the callback.
    '''
    def scrape(self):
        #TODO(Harihar): Actually implement something here.
        print "Hello world"

    '''
    Run the scraper. This will launch another thread, so make sure to terminate it by calling
    stop().
    '''
    def run(self):
        self.mutex.acquire()
        if self.thread_running:
            self.mutex.release()
            return
        self.thread_running = True
        self.ticks_until_next_scrape = self.ping_interval
        self.mutex.release()
        self.thread.start()

    '''
    Kill the scraper, if it is currently running.
    '''
    def stop(self):
        self.mutex.acquire()
        self.thread_running = False
        self.mutex.release()

    '''
    Return string representation of this object.
    '''
    def __repr__(self):
        return "Scraper(ping_interval=%d, max_imagedata_in_mem=%d)" % (self.ping_interval, self.max_imagedata_in_mem)
