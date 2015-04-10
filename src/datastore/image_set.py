import threading
import random

'''
A thread-safe in-memory set of image data items.
'''
class ImageSet:
    '''
    Create the set with a given capacity.
    '''
    def __init__(self, capacity=100000):
        self.capacity = capacity
        self.mutex = threading.Lock()
        self.image_set = set()

    '''
    Add an ImageData item to the image set.
    '''
    def add_image(self, image_data):
        with self.mutex:
            self.image_set.add(image_data)
            if len(self.image_set) > self.capacity:
                self.image_set.remove(random.choice(self.image_set))

    '''
    Pick n elements randomly from the image set. If n > len(image set), then we'll return 
    the entire image set.
    '''
    def pick_n_images(self, n):
        with self.mutex:
            return random.sample(self.image_set, min(n, len(image_set)))
