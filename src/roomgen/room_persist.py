from room import *
import psycopg2

class RoomPersist:
    def __init__(self, dbname, user):
        self.dbname = dbname
        self.user = user
        self.conn = None
        self.cursor = None
    def start(self):
        self.conn = psycopg2.connect("dbname=%s user=%s" % (self.dbname, self.user))
        self.cursor = self.conn.cursor()
    def create_tables(self):
        self.cursor.execute("DROP TABLE IF EXISTS walls;")
        self.cursor.execute("DROP TABLE IF EXISTS rooms;")
        self.cursor.execute("CREATE TABLE rooms (id uuid primary key, rotation int, room_type int);")
        self.cursor.execute("CREATE TABLE walls (room_id uuid references rooms(id), startx real, starty real, endx real, endy real);")
        self.cursor.execute("CREATE INDEX room_id_idx ON walls(room_id);")
        self.conn.commit()
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
    def get_no_wall_rooms_for_type(self, room_type):
        self.cursor.execute("SELECT * FROM rooms WHERE room_type = %s;" % (room_type,))
        self.conn.commit()
        tuples = self.cursor.fetchall()
        return [Room(t[2], t[1], room_id=t[0]) for t in tuples if len(t) == 3]
    def set_walls_for_room(self, room):
        self.cursor.execute("SELECT * FROM walls WHERE room_id = '%s';" % (room.room_id,))
        self.conn.commit()
        tuples = self.cursor.fetchall()
        walls = [Wall(t[1], t[2], t[3], t[4]) for t in tuples if len(t) == 5]
        room.walls = walls
    def finish(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
