import random

def build_museum(min_rooms = 10, max_rooms = 15):
    # 1. 
    # choose a random number of total_rooms in the museum
    total_rooms = random.randrange(min_rooms, max_rooms)
    print "Number of rooms in this museum:", total_rooms

    all_rooms = []
    
    # 2. 
    # create an initial room, and decrement total_rooms
    num_doors = random.randrange(2, 4+1) # TODO: make this smarter                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            w  
    start_room = MuseumRoom(0, 0, num_doors)
        # chooses a random number of doors for the room, and
        # assigns these doors to random subset of the walls
    all_rooms.append(start_room)
    total_rooms -= 1

    while total_rooms > 0:
        # 4. 
        # choose a random open door and add a new room to it
        (new_room_x, new_room_y) = get_new_random_location(all_rooms)
        num_doors = random.randrange(1, 4+1)
        new_room = MuseumRoom(new_room_x, new_room_y, num_doors)
        all_rooms.append(new_room)
        total_rooms -= 1

        # 5.
        # Repeat step 4 while total_rooms > 0

    # 6.
    # Examine each wall of each room.
    # If there is a door but no connecting room, remove the door
    # If there isn't a door but the connecting room has one, add a door
    fix_doors(all_rooms)

    debug_print(all_rooms)


def fix_doors(current_rooms):
    for room in current_rooms:
        # for each of North, East, South, and West, check if there's a door on that wall
        for i in xrange(0,3+1):
            direction = room.int_to_dir(i)
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
                
            # add doors where needed            
            if room_exists(new_x, new_y, current_rooms) and not room.doors[direction]:
                room.doors[direction] = True

            # remove doors where needed
            if not room_exists(new_x, new_y, current_rooms) and room.doors[direction]:
                room.doors[direction] = False



def get_new_random_location(current_rooms, override_doors = False):
    # create a list of all possible room locations
    # choose one randomly from it, and return its (x,y) coords
    # if override_doors is flagged, it will also choose from non-door walls

    possible_locations = []
    
    for room in current_rooms:
        # for each of North, East, South, and West, check if there's a door on that wall
        for i in xrange(0,3+1):
            direction = room.int_to_dir(i)
            if room.doors[direction] or override_doors:
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

                # add this new room location to the list if there isn't already one there
                if not room_exists(new_x, new_y, current_rooms):
                    possible_locations.append( (new_x, new_y) )

    #print "There are ", len(possible_locations), "possible locations"
    
    if len(possible_locations) == 0:
        print "No possible room locations! Using override_doors flag"
        return get_new_random_location(current_rooms, True)

    (final_x, final_y) = random.choice(possible_locations)
    return (final_x, final_y)


# returns whether a room exists at a given location
def room_exists(x, y, current_rooms):
    for room in current_rooms:
        if room.x == x and room.y == y:
            return True
    return False

def debug_print(current_rooms):
    for room in current_rooms:
        room.debug_print()
        

######################
# MUSEUM ROOM Data Structure
######################
class MuseumRoom:
    """Defines a single, rectangular room in a museum"""
    def __init__(self, x, y, num_doors):
        self.x = x
        self.y = y
        self.num_doors = num_doors
        self.doors = {"N":False, "E":False, "S":False, "W":False}
        self.doors = self.assign_doors(num_doors)

    def assign_doors(self, num_doors):
        if (num_doors > 4 or num_doors < 0):
            print "Invalid number of doors in one room!"
            return
        
        doors = {"N":False, "E":False, "S":False, "W":False}
        while num_doors > 0:
            wall = self.choose_random_wall()
            while (doors[wall]):
                wall = self.choose_random_wall()

            doors[wall] = True
            num_doors -= 1

        return doors

    def choose_random_wall(self):
        wall = random.choice(["N","E","S","W"])
        return wall

    # basically an enum, converts 0,1,2,3 to "N", "E", "S", "W"
    def int_to_dir(self, num):
        if (num > 3 or num < 0):
            print "Invalid door index"
            return
        
        direction_map = {0:"N", 1:"E", 2:"S", 3:"W"}
        return direction_map[num]

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
