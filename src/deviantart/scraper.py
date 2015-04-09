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
    '''
    Return string representation of this object.
    '''
    def __repr__(self):
        return "Scraper(ping_interval=%d, max_imagedata_in_mem=%d)" % (self.ping_interval, self.max_imagedata_in_mem)
