import random

'''
A museum floor plan.
'''
class Museum:
    """Defines a collection of rooms that fit together with valid doors"""
    def __init__(self):
        self.rooms = []

        # Create an initial room with 4 doors.
        self.start = Room(0,0, {
            "N": True,
            "S": True,
            "W": True,
            "E": True
        }) 
        self.rooms.append(self.start)

        # Pick a random number of rooms in the museum.
        room_limit = random.randint(3, 8)
        num_rooms_created = 0

        # Continue while we haven't hit the limit and while there are still unused doors.
        while num_rooms_created < room_limit:
            # Figure out which doors are unused.
            unused = self.unused_doors()

            # If there are no unused doors, we're done.
            if len(unused) == 0:
                break
            
            # Pick a random unused door.
            direction, room = random.choice(unused)

            # Now we need to create a room adjacent to this door. Figure out the coordinates
            # of the new room.
            x, y = self.coordinate_of_direction(direction, room)
            
            # Pick a random arrangement of doors.
            constraints = self.random_door_constraints()

            # Create the room and add it to the list of rooms.
            new_room = Room(x, y, constraints)
            self.rooms.append(new_room)
            num_rooms_created += 1

        # Delete any unused doors.
        unused = self.unused_doors()
        for direction, room in unused:
            room.doors[direction] = False

    def unused_doors(self):
        unused = []
        for room in self.rooms: # Go through each room.
            for direction in room.doors: # Go through each of the 4 walls for a given room.
                if room.doors[direction]: # If the wall has a door.
                    # Find coordinates of room in that direction, and then get the room.
                    x, y = self.coordinate_of_direction(direction, room) 
                    adjacent_room = self.room_for_coordinates(x, y)

                    # If there's no room, this is an unused door.
                    if adjacent_room is None:
                        unused.append((direction, room))
                    else:
                        # If there is indeed a room, force it to have a door.
                        opposite_dir = self.opposite_direction(direction)
                        adjacent_room.doors[opposite_dir] = True
        return unused


    def create_room(self, direction, room):
        # Figure out the coordinates of the new room.
        (x, y) = self.coords_delta(direction, room)
        constraints = self.random_door_constraints()

    def coordinate_of_direction(self, direction, room):
        deltas = {
            "N": (0, 1),
            "E": (1, 0),
            "W": (-1, 0),
            "S": (0, -1)
        }
        dx, dy = deltas[direction]
        return (room.x + dx, room.y + dy)

    def opposite_direction(self, direction):
        opposite_dir = {
            "N": "S",
            "S": "N",
            "E": "W",
            "W": "E"
        }
        return opposite_dir[direction]

    '''
    Create a random constraint object to indicate the doors.
    '''
    def random_door_constraints(self):
        num_doors = random.randint(1, 4)
        true_false_vals = num_doors * [True] + (4 - num_doors) * [False]
        random.shuffle(true_false_vals)
        return {
            "N": true_false_vals[0],
            "E": true_false_vals[1],
            "S": true_false_vals[2],
            "W": true_false_vals[3] 
        }

    # prints each room in the museum in a human-readable diagram
    def debug_print(self):
        for r in self.rooms:
            r.debug_print()

    # returns whether a room exists at a given location
    def room_for_coordinates(self, x, y):
        for r in self.rooms:
            if r.x == x and r.y == y:
                return r
        return None

######################
# ROOM Data Structure
######################
class Room:
    '''
    @param x - The x-coordinate of the room.
    @param y - The y-coordinate of the room.
    @param constraints - A dictionary indicating required doors. The keys are either "N", "S",
        "W", or "E" and the values are booleans indicating whether there should be a door there.
    '''
    def __init__(self, x, y, constraints=None):
        self.x = x
        self.y = y
        self.doors = {"N":False, "E":False, "S":False, "W":False}
        # (for now, assume that any wall without a door has an artwork)

        # if constraints[direction] is True => there must be a door on that wall
        self.constraints = {"N":False, "E":False, "S":False, "W":False}
        if constraints is not None:
            for key in constraints:
                self.constraints[key] = constraints[key]
        self.resolve_constraints()

    # creates doors on a random subset of walls. resolves constraints automatically afterwards
    def randomize_walls(self):
        for i in xrange(0,3+1):
            direction = self.int_to_dir(i)
            rand = random.choice([True, False])
            self.doors[direction] = rand
        self.resolve_constraints()

    # basically an enum, converts 0,1,2,3 to "N", "E", "S", "W"
    def int_to_dir(self, num):
        if (num > 3 or num < 0):
            print "Invalid door index"
            return
        
        direction_map = {0:"N", 1:"E", 2:"S", 3:"W"}
        return direction_map[num]

    # forces doors to appear on walls with constraints
    def resolve_constraints(self):
        for i in xrange(0,3+1):
            direction = self.int_to_dir(i)
            is_constrained = self.constraints[direction]
            if self.constraints[direction]:
                self.doors[direction] = True

    def debug_print(self):
        """ Prints a graphical representation of the room """
        
        doorN = "-"
        doorE = "|"
        doorS = "-"
        doorW = "|"

        if(self.doors["N"]):
            doorN = "D"
        if(self.doors["E"]):
            doorE = "D"
        if(self.doors["S"]):
            doorS = "D"
        if(self.doors["W"]):
            doorW = "D"
        
        print " ----" + doorN + "----"
        print "|         |"
        print doorW + "  ("+str(self.x)+","+str(self.y)+")  " + doorE
        print "|         |"
        print " ----" + doorS + "----"

