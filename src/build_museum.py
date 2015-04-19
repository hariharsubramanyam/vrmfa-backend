from roomgen.room_persist import *
from roomgen.room import *
from deviantart.imagedata import *
from deviantart.redis_store import *

class MuseumBuilder:
    '''
    @param dbname - The name of the Postgres database containing the rooms.
    @param user - The user for the Postgres database.
    @param host - The hostname for the Redis server.
    @param port - The port for the Redis server.
    @param db - The database name for the Redis server.
    '''
    def __init__(self, dbname, user, host, port, db):
        self.redis_store = RedisStore(host, post, db)
        self.room_store = RoomPersist(dbname, user)
        self.room_store.start()

    '''
    Attempt to fill the rooms with paintings on their walls.

    Returns True if all the walls were filled with paintings. If the Redis cache does not have
    enough paintings, we cannot fill all the walls, so we return False.
    '''
    def fill_rooms_with_paintings(self, rooms):
        num_needed_paintings = sum([len(room.walls) for room in rooms])
        paintings = self.redis_store.pick_n_images(num_needed_paintings)
        painting_index = 0
        for room in rooms:
            for wall in room.walls:
                wall.image_data = paintings[painting_index]
                painting_index += 1
        return num_needed_paintings == painting_index
