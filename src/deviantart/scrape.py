from models.imagedata import ImageData

'''
The implementation which is actually responsible for fetching the HTML from DeviantArt and turning
it into ImageData objects.
'''
class ScrapeImplementation:
    '''
    Perform the scrape. This does not need to handle de-duplication of ImageData between calls.

    @return a list of ImageData objects.
    '''
    def scrape(self):
        return [ImageData("www.google.com")]
