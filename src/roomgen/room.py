import uuid
'''
An enum that represents all possible arrangements of doors in a room. Note that we consider two rooms
identical if one can be rotated to get the other.

north = A single door on the north wall.
north_east = Two doors - one on the north, one on the east.
north_south = Two doors - one on the north, one on the south.
north_east_south = Three doors - only the west wall has no door.
north_east_south_west = Four doors - all walls have doors.
'''
class RoomType:
    north = 1
    north_east = 2
    north_south = 3
    north_east_south = 4
    north_east_south_west = 5

'''
Represents a rotation of a room.
'''
class Rotation:
    clockwise0 = 0
    clockwise90 = 90
    clockwise180 = 180
    clockwise270 = 270

'''
Determine the room type and the rotation for a given arrangement of doors.

@param north (bool) - whether the room has door on the north wall.
@param east (bool) - whether the room has door on the east wall.
@param south (bool) - whether the room has door on the south wall.
@param west (bool) - whether the room has door on the west wall.

At least one of north, east, south, or west must be True. 

@return (room_type, rotation) - room_type is a RoomType and rotation is a Rotation. The given
    room_type, when rotated by rotation degrees will have the arrangement of doors as prescribed
    by north, east, south, and west.
'''
def compute_rotated_room(north, east, south, west):
    # Count the number of doors in the room.
    num_doors = len([x for x in (north, east, south, west) if x])

    # Handle the error case.
    if num_doors == 0:
        raise Exception("You can't have a room with 0 doors!")

    # Figure out the room type based on the door count (and, if necessary, the arrangement of doors).
    # Also compute the rotation.
    room_type = None
    rotation = None
    if num_doors == 1:
        room_type = RoomType.north
        # Figure out which wall has the single door and rotate accordingly.
        if north:
            rotation = Rotation.clockwise0
        elif east:
            rotation = Rotation.clockwise90
        elif south:
            rotation = Rotation.clockwise180
        elif west:
            rotation = Rotation.clockwise270
    elif num_doors == 3:
        room_type = RoomType.north_east_south
        # Figure out which wall does NOT have a door and rotate accordingly.
        if not west:
            rotation = Rotation.clockwise0
        elif not north:
            rotation = Rotation.clockwise90
        elif not east: 
            rotation = Rotation.clockwise180
        elif not south:
            rotation = Rotation.clockwise270
    elif num_doors == 4:
        room_type = RoomType.north_east_south_west
        # Since all walls have doors, there's no need to rotate.
        rotation = Rotation.clockwise0
    elif num_doors == 2:
        # In this case, we need to check if the doors are opposite each other or adjacent to each
        # other.
        if (north and south) or (east and west):
            room_type = RoomType.north_south
            # Figure out which pair of rooms has the doors, then rotate accordingly.
            if north and south:
                rotation = Rotation.clockwise0
            elif east and west:
                rotation = Rotation.clockwise90
        else:
            room_type = RoomType.north_east
            # Figure out which pair of rooms has the doors, then rotate accordingly.
            if north and east:
                rotation = Rotation.clockwise0
            elif east and south:
                rotation = Rotation.clockwise90
            elif south and west:
                rotation = Rotation.clockwise180
            elif west and north:
                rotation = Rotation.clockwise270

    # Ensure that the above logic managed to compute the room type and rotation.
    if room_type is None or rotation is None:
        raise Exception("Failed to compute room type and rotation for (%s, %s, %s, %s)" % (north, east, south, west))

    return room_type, rotation

'''
Represents a wall in the room. 
'''
class Wall:
    '''
    @param startx - The x coordinate that starts the wall. It must be between 0 and 1.
    @param starty - The y coordinate that starts the wall. It must be between 0 and 1.
    @param endx - The x coordinate that ends the wall. It must be between 0 and 1.
    @param endy - The y coordinate that ends the wall. It must be between 0 and 1.
    @param image_data - The ImageData object on this wall.
    '''
    def __init__(self, startx, starty, endx, endy, image_data=None):
        def out_of_bounds(x, y):
            return x < 0 or x > 1 or y < 0 or y > 1
        if out_of_bounds(startx, starty) or out_of_bounds(endx, endy):
            raise Exception("The wall (%s, %s) -> (%s, %s) is out of bounds", startx, starty, endx, endy)
        self.startx = startx
        self.starty = starty
        self.endx = endx
        self.endy = endy
        self.image_data = image_data 
    def __str__(self):
        return "Wall((%s, %s) -> (%s, %s), image_data=%s)" % (self.startx, self.starty, self.endx, self.endy, self.image_data)
    __repr__ = __str__

'''
Represents a room in a museum.
'''
class Room:
    '''
    @param room_type - A room type as defined in RoomType.
    @param walls - A list of Wall objects.
    @param rotation - A rotation as defined in Rotation.
    @param room_id - An unique identifier for the room.
    '''
    def __init__(self, room_type, rotation, walls=None, room_id=None):
        if room_id is None:
            self.room_id = uuid.uuid4().hex
        else:
            self.room_id = room_id
        self.room_type = room_type
        self.rotation = rotation
        if walls is None:
            self.walls = []
        else:
            self.walls = walls
    def __str__(self):
        return "Room(id=%s, rotation=%s, room_type=%s, walls=%s)" % (self.room_id, self.rotation, self.room_type, self.walls)
    __repr__ = __str__
