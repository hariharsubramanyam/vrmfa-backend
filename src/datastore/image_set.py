import random

'''
An in-memory set of image data items.
'''
class ImageSet:
    '''
    Create the set with a given capacity.
    '''
    def __init__(self, capacity=100000):
        self.capacity = capacity
        self.image_set = set()

    '''
    Add an ImageData item to the image set.
    @param image_data - The ImageData to add to the set.
    @param The item that was deleted in order to make room for the new addition, or None if there
        was no deletion.
    '''
    def add_image(self, image_data):
        self.image_set.add(image_data)
        if len(self.image_set) > self.capacity:
            deleted = random.choice(self.image_set)
            self.image_set.remove(deleted)
            return deleted

    '''
    Pick n elements randomly from the image set. If n > len(image set), then we'll return 
    the entire image set.
    '''
    def pick_n_images(self, n):
        return random.sample(self.image_set, min(n, len(image_set)))
