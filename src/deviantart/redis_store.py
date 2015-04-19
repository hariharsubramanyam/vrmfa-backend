import redis
from imagedata import ImageData

class RedisStore:
    def __init__(self, host, port, db, capacity=10000, expiry_time=24*60*60, set_name="images"):
        self.capacity = capacity
        self.expiry_time = expiry_time
        self.set_name = set_name
        self.redis = redis.StrictRedis(host=host, port=port, db=db)
    def add_image(self, image_data):
        self.redis.sadd(self.set_name, image_data.serialize())
        set_size = self.redis.scard(self.set_name)
        while set_size > self.capacity:
            self.redis.spop(self.set_name)
            set_size = self.redis.scard(self.set_name)
    def pick_n_images(self, n):
        set_size = self.redis.scard(self.set_name)
        random_members = self.redis.srandmember(self.set_name, min(n, set_size))
        return [ImageData(None, None).deserialize(x) for x in random_members]
