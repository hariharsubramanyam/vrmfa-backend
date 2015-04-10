'''
Represents the data for one image pulled from DeviantArt.
'''
class ImageData:
    '''
    @param url - The url to the image on DeviantArt.
    '''
    def __init__(self, url):
        self.url = url

    '''
    Return string representation of this object.
    '''
    def __repr__(self):
        return str(self.url)

    def serialize(self):
        return str(self.url)

    def deserialize(self, string):
        self.url = string
