from room import *
import json
import psycopg2

'''
Helper class for storing and retrieving rooms from a Postgres database.

Make sure you call start() to begin operation and that you call finish() when you are done.
'''
class RoomPersist:
    '''
    Create the object with the given database and user. This constructor doesn't actually 
    create the connnection. You need to call start() to create the connection (and finish() will
    end the connection).
    '''
    def __init__(self, dbname, user):
        self.dbname = dbname
        self.user = user
        self.conn = None
        self.cursor = None
    '''
    Connect to the databse.
    '''
    def start(self):
        self.conn = psycopg2.connect("dbname=%s user=%s" % (self.dbname, self.user))
        self.cursor = self.conn.cursor()
    '''
    Create the tables. If they already exist, this will delete them and recreate them.
    '''
    def create_tables(self):
        self.cursor.execute("DROP TABLE IF EXISTS walls;")
        self.cursor.execute("DROP TABLE IF EXISTS rooms;")
        self.cursor.execute("CREATE TABLE rooms (id uuid primary key, rotation int, room_type int);")
        self.cursor.execute("CREATE TABLE walls (room_id uuid references rooms(id), startx real, starty real, endx real, endy real);")
        self.cursor.execute("CREATE INDEX room_id_idx ON walls(room_id);")
        self.conn.commit()
    '''
    Persist the room in the database. If the room is already in the database, it will be deleted
    and then inserted.
    '''
    def persist_room(self, room):
        # Get rid of the room if it exists.
        self.cursor.execute("DELETE FROM walls where room_id = '%s';" % (room.room_id,))
        self.cursor.execute("DELETE FROM rooms where id = '%s';" % (room.room_id,))
        # Persist the rooms data.
        self.cursor.execute("INSERT INTO rooms (id, room_type, rotation) VALUES ('%s', %d, %d);"
                % (room.room_id, room.room_type, room.rotation))
        self.conn.commit()
        # Now persist the walls.
        if len(room.walls) == 0:
            return
        wall_query_fmt = "INSERT INTO walls (room_id, startx, starty, endx, endy) VALUES %s;"
        wall_strings = []
        for wall in room.walls:
            wall_strings.append("('%s', %s, %s, %s, %s)" % 
                    (room.room_id, wall.startx, wall.starty, wall.endx, wall.endy))
        wall_query = wall_query_fmt % (", ".join(wall_strings))
        self.cursor.execute(wall_query)
        self.conn.commit()
    '''
    Return all the rooms with the given types. Their walls will not be retrieved, so you will need
    to call set_walls_for_room(room) for each of the room objects populate their walls.
    '''
    def get_no_wall_rooms_for_type(self, room_type):
        self.cursor.execute("SELECT * FROM rooms WHERE room_type = %s;" % (room_type,))
        self.conn.commit()
        tuples = self.cursor.fetchall()
        return [Room(t[2], t[1], room_id=t[0]) for t in tuples if len(t) == 3]
    '''
    Given a Room object, look up its walls in the database and populate the walls array.
    '''
    def set_walls_for_room(self, room):
        self.cursor.execute("SELECT * FROM walls WHERE room_id = '%s';" % (room.room_id,))
        self.conn.commit()
        tuples = self.cursor.fetchall()
        walls = [Wall(t[1], t[2], t[3], t[4]) for t in tuples if len(t) == 5]
        room.walls = walls
    '''
    Load the data from the json file and persist it.
    '''
    def persist_default_room_set(self, file_path):
        data = json.load(open(file_path))
        rooms = []
        for room_data in data["data"]:
            room_type = room_data["type"]
            walls = room_data["walls"]
            walls = [Wall(wall[0][0], wall[0][1], wall[1][0], wall[1][1]) for wall in walls]
            room = Room(room_type, Rotation.clockwise0, walls=walls)
            rooms.append(room)
        for room in rooms:
            self.persist_room(room)
    '''
    Close the connection to the database.
    '''
    def finish(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
