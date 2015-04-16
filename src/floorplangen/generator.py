import random

######################
# TESTS
######################

# creates 5 random rooms
def test_random_walls():
    r = Room(0,0)
    print "Ititial doors: ", r.doors
    for i in xrange(0,5):
        r.randomize_walls()
        r.debug_print()

# creates and debug-prints a museum
def test_museum():
    m = Museum()

######################
# MUSEUM Data Structure
######################
class Museum:
    """Defines a collection of rooms that fit together with valid doors"""
    def __init__(self):
        self.rooms = []
        # create an initial room in the southeast corner of the museum
        self.start = Room(0,0,{"N":True,"E":True,"S":False,"W":False})
        self.rooms.append(self.start)
        
        self.rooms_with_adjacents = []
        # create adjacent rooms in a BFS order
        i = 0
        while i < len(self.rooms) and i < 30:
            self.create_adjacent_rooms(self.rooms[i])
            i += 1
        
        self.debug_print()

    # prints each room in the museum in a human-readable diagram
    def debug_print(self):
        for r in self.rooms:
            r.debug_print()

    # given a room, looks at each of its doors and creates a new room where needed
    def create_adjacent_rooms(self, room):
        # ensure we don't re-create rooms that have already been created
        if room in self.rooms_with_adjacents:
            print "adjacents have already been created for room (" + str(room.x) + "," + str(room.y) + ")"
            return

        # for each of North, East, South, and West, check if there's a door on that wall
        for i in xrange(0,3+1):
            direction = room.int_to_dir(i)
            if room.doors[direction]:
                new_x = room.x
                new_y = room.y
                if i == 0:
                    new_y += 1
                elif i == 1:
                    new_x += 1
                elif i == 2:
                    new_y -= 1
                elif i == 3:
                    new_x -= 1

                # ensures that doors are created if connecting rooms have doors
                constraints = self.get_constraints(new_x,new_y)

                # creates a new room in the location if there isn't already a room there
                if not self.room_exists(new_x, new_y):
                    new_room = Room(new_x, new_y, constraints)
                    new_room.randomize_walls()
                    self.rooms.append(new_room)
                    
        self.rooms_with_adjacents.append(room)

    # returns whether a room exists at a given location
    def room_exists(self, x, y):
        for r in self.rooms:
            if r.x == x and r.y == y:
                return True
        return False

    # returns which wall directions must have a door (because a door exists in an adjacent room)
    def get_constraints(self, x, y):
        constraints = {}

        exists_door_N = False
        exists_door_E = False
        exists_door_S = False
        exists_door_W = False

        for r in self.rooms:
            if r.x == x and r.y == y+1:
                exists_door_N = True
            if r.x == x+1 and r.y == y:
                exists_door_E = True
            if r.x == x and r.y == y-1:
                exists_door_S = True
            if r.x == x-1 and r.y == y:
                exists_door_W = True
        
        if exists_door_N:
            constraints["N"] = True
        if exists_door_E:
            constraints["E"] = True
        if exists_door_S:
            constraints["S"] = True
        if exists_door_W:
            constraints["W"] = True
            
        return constraints

######################
# ROOM Data Structure
######################
class Room:
    """Defines a single, rectangular room in a museum"""
    def __init__(self, x, y, constraints=None):
        self.x = x
        self.y = y
        self.doors = {"N":False, "E":False, "S":False, "W":False}
        # (for now, assume that any wall without a door has an artwork)

        # if constraints[direction] implies => there must be a door on that wall
        self.constraints = {"N":False, "E":False, "S":False, "W":False}
        if(constraints):
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
            if (is_constrained):
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

