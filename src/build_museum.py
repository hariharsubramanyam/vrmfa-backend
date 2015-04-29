from roomgen.room_persist import *
from roomgen.room import *
from deviantart.imagedata import *
from deviantart.redis_store import *
from museumpersist.persist import *
from floorplangen.generator import Museum
from datetime import *
import random
import json

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
    museum_persist = Persist(dbname, user)
    museum_persist.start()

    # Figure out the day.
    today = datetime.today()
    year = today.year
    month = today.month
    day = today.day

    # Check if the museum already exists.
    stored_museum = museum_persist.get_museum(year, month, day)
    if stored_museum is not None:
        room_store.finish()
        museum_persist.finish()
        return rooms_from_json(stored_museum)

    museum_rooms = []
    floor_plan = Museum()
    for room in floor_plan.rooms:
        room_type, rotation = compute_rotated_room(room.doors["N"], room.doors["E"], room.doors["S"], room.doors["W"])
        possible_rooms = room_store.get_no_wall_rooms_for_type(room_type)
        if len(possible_rooms) == 0:
            room_store.persist_default_room_set("./roomgen/room_data.json")
            possible_rooms = room_store.get_no_wall_rooms_for_type(room_type)
        chosen_room = random.choice(possible_rooms)
        chosen_room.rotation = rotation
        chosen_room.x = room.x
        chosen_room.y = room.y
        room_store.set_walls_for_room(chosen_room)
        museum_rooms.append(chosen_room)

    fill_rooms_with_paintings(museum_rooms, paintings_redis)

    rooms_json = rooms_to_json(museum_rooms)
    museum_persist.persist_museum(year, month, day, rooms_json)
    room_store.finish()
    museum_persist.finish()
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

def rooms_to_json(rooms):
    result = json.dumps({
        "rooms": [room.to_json_dict() for room in rooms]
    })
    return result

def rooms_from_json(rooms_string):
    rooms_json = json.loads(rooms_string)
    rooms = rooms_json["rooms"]
    room_objs = []
    for room in rooms:
        room_id = room["room_id"]
        x = room["x"]
        y = room["y"]
        rotation = room["rotation"]
        room_type = room["room_type"]
        walls = room["walls"]
        wall_objs = []
        for wall in walls:
            startx = wall["startx"]
            starty = wall["starty"]
            descr = wall["descr"]
            endy = wall["endy"]
            endx = wall["endx"]
            url = wall["url"]
            image_data = ImageData(url, descr)
            wall_obj = Wall(startx, starty, endx, endy, image_data=image_data)
            wall_objs.append(wall_obj)
        room_obj = Room(room_type, rotation)
        room_obj.room_id = room_id
        room_obj.walls = wall_objs
        room_obj.x = x
        room_obj.y = y
        room_objs.append(room_obj)
    return room_objs


if __name__=="__main__":
    museum_rooms = build_museum('vrmfa', 'harihar', 'localhost', 6379, 0)
    print rooms_to_json(museum_rooms)
