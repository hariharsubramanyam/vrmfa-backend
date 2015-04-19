import json

'''
Represents the data for one image pulled from DeviantArt.
'''
class ImageData:
    def __init__(self, url, descr):
        self.url = url
        self.descr = descr

    '''
    Return string representation of this object.
    '''
    def __repr__(self):
        return "ImageData(descr=%s, url=%s)" % (self.descr, self.url)

    def serialize(self):
        return json.dumps({"descr": self.descr, "url": self.url})

    def deserialize(self, string):
        deserialized_json = json.loads(string)
        self.descr = deserialized_json["descr"]
        self.url = deserialized_json["url"]
        return self
