from roomgen.room_persist import *
from roomgen.room import *
from deviantart.imagedata import *
from deviantart.redis_store import *
from floorplangen.generator import *
import random

'''
@param dbname - The name of the Postgres database containing the rooms.
@param user - The user for the Postgres database.
@param host - The hostname for the Redis server.
@param port - The port for the Redis server.
@param db - The database name for the Redis server.
'''
def build_museum(dbname, user, host, port, db):
    paintings_redis = RedisStore(host, port, db)
    room_store = RoomPersist(dbname, user)
    room_store.start()

    museum_rooms = []
    floor_plan = Museum()
    for room in floor_plan.rooms:
        room_type, rotation = compute_rotated_room(room.doors["N"], room.doors["E"], room.doors["S"], room.doors["W"])
        possible_rooms = room_store.get_no_wall_rooms_for_type(room_type)
        if len(possible_rooms) == 0:
            raise Exception("There are no rooms :(")
        chosen_room = random.choice(possible_rooms)
        room_store.set_walls_for_room(chosen_room)
        fill_rooms_with_paintings(chosen_room)
        museum_rooms.append(chosen_room)

    room_store.finish()
    return museum_rooms

'''
Attempt to fill the rooms with paintings on their walls.

Returns True if all the walls were filled with paintings. If the Redis cache does not have
enough paintings, we cannot fill all the walls, so we return False.
'''
def fill_rooms_with_paintings(rooms, paintings_redis):
    num_needed_paintings = sum([len(room.walls) for room in rooms])
    paintings = paintings_redis.pick_n_images(num_needed_paintings)
    painting_index = 0
    for room in rooms:
        for wall in room.walls:
            wall.image_data = paintings[painting_index]
            painting_index += 1
    return num_needed_paintings == painting_index

if __name__=="__main__":
    museum_rooms = build_museum('vrmfa', 'harihar', 'localhost', 6379, 0)
    print museum_rooms
